import os
import json
import random
from fastapi import FastAPI, HTTPException, Response
from consistent_hash import ConsistentHashMap
import docker
import re



app = FastAPI()

# Create an instance of the Docker client
docker_client = docker.from_env()

# Create an instance of the consistent hash map
consistent_hash_map = ConsistentHashMap()

# Add initial server replicas to the consistent hash map
# for server_id in range(1, 4):  # Assuming initial N=3
#     container = docker_client.containers.run("fastapi:latest", detach=True, remove=True, name=f"server{server_id}", environment={"ROLE": "server", "SERVER_ID": str(server_id)}, network="fastapi_default", network_alias=f"server{server_id}")
#     consistent_hash_map.add_server(server_id, container.name)

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

@app.get("/home")
async def home():
    server_id = get_server_id()
    if server_id is None:
        response_data = {
            "message": "Server ID not available",
            "status": "failure"
        }
        return Response(content=json.dumps(response_data), media_type="application/json", status_code=503)
    else:
        message = f"Hello from Server: {server_id}"
        response_data = {
            "message": message,
            "status": "successful"
        }
        return Response(content=json.dumps(response_data), media_type="application/json", status_code=200)
     



@app.get("/heartbeat")
async def heartbeat():
    """
    Heartbeat endpoint to check server availability.
    Returns a successful response (HTTP 200 OK) if the server is available.
    """
    status_code = 200
    response_data = {
        "status": "OK",
        "status_code": status_code
    }
    return Response(content=json.dumps(response_data), status_code=status_code, media_type="application/json")