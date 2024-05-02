import os
import json
import requests
from fastapi import FastAPI, HTTPException, Response
from consistent_hash import ConsistentHashMap
import docker
import re



app = FastAPI()

# Create an instance of the Docker client
docker_client = docker.from_env()

# Create an instance of the consistent hash map
consistent_hash_map = ConsistentHashMap()

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ... (existing code) ...
# Retrieve the server instances created by Docker Compose
network_name = os.environ.get("COMPOSE_PROJECT_NAME", "ds-assignment_implementing-a-load-balancer") + "_app_network"
logging.info(f'Retrieving server instances from network: {network_name}')
server_containers = docker_client.containers.list(filters={'network': network_name})
logging.info(f'Found {len(server_containers)} instances: {[container.name for container in server_containers]}')

# Add the server instances to the consistent hash map
for i, container in enumerate(server_containers, start=1):
    container_name = container.name
    if "load_balancer" not in container_name:
        server_id = i
        container_port = 8000  # Assuming the server instances are running on port 8000
        consistent_hash_map.add_server(server_id, container_name, container_port)
        logging.info(f'Adding server instance {container_name} with ID {server_id} to the consistent hash map')
    else:
        logging.info(f'Skipping load balancer instance {container_name}')

logging.info('Initial server instances added to the consistent hash map')

def update_environment_variables():
    # Update environment variables based on consistent hash map
    os.environ["N_SERVERS"] = str(len(consistent_hash_map.servers))
    os.environ["NUM_SLOTS"] = str(consistent_hash_map.NUM_SLOTS)
    os.environ["NUM_VIRTUAL_SERVERS"] = str(consistent_hash_map.NUM_VIRTUAL_SERVERS)


def get_server_id():
    server_id = os.environ.get("SERVER_ID")
    if not server_id:
        raise ValueError("SERVER_ID environment variable is not set")
    return server_id

@app.get("/rep")
async def get_replicas():
    replicas = list(consistent_hash_map.servers.values())
    server_names = [server_name for server_name, _, _ in replicas]
    response_data = {
        "message": {
            "N": len(server_names),
            "replicas": server_names
        },
        "status": "successful"
    }
    return Response(content=json.dumps(response_data), media_type="application/json")


import uuid

import random
@app.post("/add")
async def add_replicas(payload: dict):
    n = payload.get("n", 0)
    hostnames = payload.get("hostnames", [])

    # Sanity check: Ensure 'n' is a positive integer
    if not isinstance(n, int) or n <= 0:
        raise HTTPException(status_code=400, detail="'n' must be a positive integer")

    # Log the hostnames provided in the payload
    print("Hostnames to add:", hostnames)

    # Convert all server names to lowercase and strip leading/trailing whitespaces
    existing_server_names = {server_name.strip().lower(): server_id for server_id, (server_name, _) in consistent_hash_map.servers.items()}

    # Check if the total number of hostnames matches the specified count 'n'
    if len(hostnames) != n:
        raise HTTPException(status_code=400, detail=f"The number of hostnames provided ({len(hostnames)}) does not match the specified count ({n})")

    # Check each individual hostname to ensure it is unique and not already present in the consistent hash map
    new_server_ids = []
    new_server_names = []
    for hostname in hostnames:
        stripped_hostname = hostname.strip().lower()
        if stripped_hostname in existing_server_names:
            raise HTTPException(status_code=409, detail=f"Server '{stripped_hostname}' already exists")
        # Assign a new server ID
        new_server_id = max(existing_server_names.values(), default=0) + 1
        new_server_ids.append(new_server_id)
        new_server_names.append(stripped_hostname)
        existing_server_names[stripped_hostname] = new_server_id

    # Log the new server IDs
    print("New Server IDs:", new_server_ids)

    # Get the running container instance (assuming there's at least one)
    existing_containers = docker_client.containers.list(filters={'status': 'running'})
    if not existing_containers:
        raise HTTPException(status_code=500, detail="No running container found to duplicate")

    # Use the first running container as the template
    template_container = existing_containers[0]

    # Create a new network with a unique name
    new_network_name = f"server_network_{uuid.uuid4().hex}"
    new_network = docker_client.networks.create(new_network_name, driver="bridge")

    # Create new containers by duplicating the template
    for i in range(n):
        hostname = hostnames[i].strip().lower()
        hostname = hostname.replace(" ", "-")  # Replace spaces with dashes
        hostname = re.sub(r"[^a-zA-Z0-9_.-]", "", hostname)  # Remove invalid characters
        server_id = len(consistent_hash_map.servers) + 1

        # Create a new container with the same configuration as the template container
        new_container = docker_client.containers.create(
            image=template_container.image.tags[0],
            name=hostname,
            environment={"SERVER_ID": str(server_id)},
            network=new_network_name,
            ports={'4000/tcp': None}  # Use dynamic port mapping for port 3000
        )
        new_container.start()

        # Get the assigned host port for the new container
        host_port = new_container.attrs['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']

        consistent_hash_map.add_server(server_id, (hostname, host_port))

    # Get the updated replicas after addition
    replicas = list(consistent_hash_map.servers.keys())
    response_data = {
        "message": {
            "N": len(replicas),
            "replicas": [consistent_hash_map.servers[server_id][0].name for server_id in replicas]
        },
        "status": "successful"
    }
    return Response(content=json.dumps(response_data), media_type="application/json")

@app.delete("/rm")
async def remove_replicas(payload: dict):
    n = payload.get("n", 0)
    hostnames = payload.get("hostnames", [])

    # Sanity check: Ensure 'n' is a positive integer
    if not isinstance(n, int) or n <= 0:
        raise HTTPException(status_code=400, detail="'n' must be a positive integer")

    # Log the hostnames provided in the payload
    print("Hostnames to remove:", hostnames)

    # Convert all server names to lowercase and strip leading/trailing whitespaces
    server_names = {server_name.strip().lower(): server_id for server_id, (server_name, _) in consistent_hash_map.servers.items()}

    # Check if the total number of hostnames matches the specified count 'n'
    if len(hostnames) != n:
        raise HTTPException(status_code=400, detail=f"The number of hostnames provided ({len(hostnames)}) does not match the specified count ({n})")

    # Check each individual hostname to ensure it exists in the consistent hash map
    server_ids_to_remove = []
    for hostname in hostnames:
        stripped_hostname = hostname.strip().lower()
        server_id = server_names.get(stripped_hostname)
        if server_id is None:
            raise HTTPException(status_code=404, detail=f"Server '{stripped_hostname}' specified for removal is not found")
        server_ids_to_remove.append(server_id)

    # Log the filtered server IDs
    print("Filtered Server IDs to remove:", server_ids_to_remove)

    # Get the server IDs to remove based on the provided hostnames
    server_ids_to_remove = [
        server_id for server_id, (container_name, _) in consistent_hash_map.servers.items()
        if container_name in hostnames
    ]

    # Remove the servers from the consistent hash map
    for server_id in server_ids_to_remove:
        consistent_hash_map.remove_server(server_id)


    # Get the remaining replicas after removal
    replicas = list(consistent_hash_map.servers.keys())
    response_data = {
        "message": {
            "N": len(replicas),
            "replicas": [f"Server {server_id}" for server_id in replicas]
        },
        "status": "successful"
    }
    return Response(content=json.dumps(response_data), media_type="application/json")




# ...

@app.get("/{path:path}")
async def route_request(path: str):
    # Generate a random request ID for demonstration purposes
    import random
    request_id = random.randint(100000, 999999)

    # Get the server ID using consistent hashing
    server_id = consistent_hash_map.get_server(request_id)

    if server_id is None:
        response_data = {
            "message": "<Error> No server available to handle the request",
            "status": "failure"
        }
        return Response(content=json.dumps(response_data), media_type="application/json", status_code=503)

    # Get the server container name and port
    container_name, _, container_port = consistent_hash_map.servers[server_id]

    # Check if the server is available by sending a heartbeat request
    server_url = f"http://{container_name}:{container_port}/heartbeat"
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            # Server is available, route the request
            request_url = f"http://{container_name}:{container_port}/{path}"
            response = requests.get(request_url)

            if path == "home":
                # Return the response from the server's /home endpoint
                return Response(content=response.content, media_type=response.headers['Content-Type'], status_code=response.status_code)
            else:
                # Return an error for endpoints not registered with the web server
                response_data = {
                    "message": f"<Error> '/{path}' endpoint does not exist in server replicas",
                    "status": "failure"
                }
                return Response(content=json.dumps(response_data), media_type="application/json", status_code=400)
        else:
            # Server is unavailable
            response_data = {
                "message": f"<Error> Server {container_name} is unavailable",
                "status": "failure"
            }
            return Response(content=json.dumps(response_data), media_type="application/json", status_code=503)
    except requests.exceptions.RequestException as e:
        # Error connecting to the server
        response_data = {
            "message": f"<Error> Failed to connect to server {container_name}: {str(e)}",
            "status": "failure"
        }
        return Response(content=json.dumps(response_data), media_type="application/json", status_code=503)
