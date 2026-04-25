from server import Server
from client import Client

"""
Orchestrates the communication and data transfer between the Server and Client nodes.
"""
class Connection:
    """
    Initializes the connection, creates nodes, and exchanges public keys.
    """
    def __init__(self):
        self.server = Server()
        self.client = Client()
        self.server.set_client_public_key(self.client.public_key)
        self.client.set_server_public_key(self.server.public_key)
        self.establish_connection()

    """
    Runs the command-line interface for the user to interact with the system.
    """
    def command_line(self):
        while True:
            print("\nAvailable commands:")
            print("1. offload - Offload data from server to client")
            print("2. retrieve - Retrieve data from server")
            print("3. exit - Exit the program")
            
            command = input("Enter command: ")
            
            match command:
                case "offload":
                    failState = self._get_bool_input("Enter fail state for offload (true/false): ")
                    if failState is None:
                        continue
                    self.data_offload(failState)
                case "retrieve":
                    failState = self._get_bool_input("Enter fail state for retrieval (true/false): ")
                    if failState is None:
                        continue
                    self.data_retrieve(failState)
                case "exit":
                    print("Exiting...")
                    break
                case _:
                    print("Invalid command. Please try again.")
    
    """
    Logs the initialization status of the system nodes.
    """
    def establish_connection(self):
        print("System nodes initialized. Command line interface ready.")
    
    """
    Handles the data offload process from server to client.
    
    @param state: Boolean indicating if a failure should be simulated during transfer.
    """
    def data_offload(self, state):
        print("Starting data offload process...")
        # Server prepares data and computes hash
        data, signature = self.server.offload()
        
        # Connection passes data to client
        success = self.client.receive_data(state, (data, signature))

        print(f"Eve sees data: {data} and signature: {signature.hex()}")
        
        if success:
            print("Data offload successful with failstate: ", state)
        else:
            print("Data offload failed with failstate: ", state)

    """
    Handles the data retrieval process from client back to server.
    
    @param state: Boolean indicating if corrupted data should be sent by the client.
    """
    def data_retrieve(self, state):
        print("Starting data retrieval process...")
        # Client sends data back to server
        data, signature = self.client.send_data(state)
        
        # Connection passes data to server for verification
        success = self.server.retrieve((data, signature))

        print(f"Eve sees data: {data} and signature: {signature.hex()}")
        
        if success:
            print("Data retrieval successful with failstate: ", state)
        else:
            print("Data retrieval failed with failstate: ", state)

        
    """
    Helper method to prompt the user for a boolean input.
    
    @param prompt: The message to display to the user.
    @return: True, False, or None if the input is invalid.
    """
    def _get_bool_input(self, prompt):
        intake = input(prompt).lower()
        if intake == "true":
            return True
        elif intake == "false":
            return False
        else:
            print("Invalid input. Please enter 'true' or 'false'.")
            return None

start = Connection()
start.command_line()

    
