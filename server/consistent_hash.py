# Number of Server Containers managed by the load balancer (N)
N_SERVERS = 3

# Total number of slots in the consistent hash map (#slots)
NUM_SLOTS = 512

# Number of virtual servers for each server container (K)
NUM_VIRTUAL_SERVERS = 9

# Hash function for request mapping
def hash_request(request_id):
    return (request_id ** 2 + 2 * request_id + 17) % NUM_SLOTS

# Hash function for virtual server mapping
def hash_virtual_server(server_id, virtual_server_id):
    return (server_id + virtual_server_id + 2 * virtual_server_id + 25) % NUM_SLOTS

# consistent_hash.py

class ConsistentHashMap:
    def _init_(self):
        self.hash_map = [[[] for _ in range(NUM_SLOTS)]]
        self.servers = {}  # {server_id: (container_name, [virtual_server_slots])}

    def add_server(self, server_id, container_name):
        """
        Add a new server to the consistent hash map.

        Args:
            server_id (int): The unique identifier for the server.
            container_name (str): The name of the Docker container for the server.
        """
        virtual_server_slots = []
        for virtual_server_id in range(NUM_VIRTUAL_SERVERS):
            slot = hash_virtual_server(server_id, virtual_server_id)
            self.hash_map[0][slot].append((server_id, container_name))
            virtual_server_slots.append(slot)
        self.servers[server_id] = (container_name, virtual_server_slots)

    def remove_server(self, server_id):
        """
        Remove a server from the consistent hash map.

        Args:
            server_id (int): The unique identifier of the server to be removed.
        """
        if server_id not in self.servers:
            return

        container_name, virtual_server_slots = self.servers.pop(server_id)
        print(f"Removing server {server_id} ({container_name})")

        for slot in virtual_server_slots:
            # Remove the server based on the provided server_id
            self.hash_map[0][slot] = [entry for entry in self.hash_map[0][slot] if entry[0] != server_id]


    def get_server(self, request_id):
        """
        Get the server ID for a given request using consistent hashing.

        Args:
            request_id (int): The unique identifier of the request.

        Returns:
            int: The server ID for the request, or None if no server is available.
        """
        slot = hash_request(request_id)
        print("Slot:", slot)

        for server_id, server_name in self.hash_map[0][slot]:
            print("Server in Slot:", server_id, server_name)
            return server_id

        # If no server is found in the current slot, probe the next slots
        for i in range(1, NUM_SLOTS):
            slot = (slot + i) % NUM_SLOTS
            if self.hash_map[0][slot]:
                server_id, server_name = self.hash_map[0][slot][0]
                print("Server in Probed Slot:", server_id, server_name)
                return server_id

        # No server available
        return None

    def print_servers(self):
        """
        Print all servers along with their IDs, names, and ports.
        """
        print("Servers:")
        for server_id, (server_name, virtual_server_slots, server_port) in self.servers.items():
            print(f"Server ID: {server_id}, Server Name: {server_name}, Server Port: {server_port}")
