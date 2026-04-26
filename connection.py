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
        self.displayMode = True

    """
    Runs the command-line interface for the user to interact with the system.
    """
    def command_line(self):
        while True:
            print("\nAvailable commands:")
            print("1. offload - Offload data from server to client")
            print("2. retrieve - Retrieve data from server")
            print("3. db_pinger - Test database connectivity")
            print("4. mallory_attempt - Attempt to intercept and modify data")
            print("5. display_server - Display server internal state")
            print("6. set_state - Set fail state for operations")
            print("7. set_display - Set display mode")
            print("8. fail_example - Simulate a failure scenario")
            print("9. success_example - Simulate a successful scenario")
            print("10. full_display - Simulate both failure and success scenarios")
            print("11. exit - Exit the program")
            print("12. reset - Reset system state")

            command = input("Enter command: ")
            
            match command:
                case "1" | "offload":
                    failState = self._get_bool_input("Enter fail state for offload (true/false): ")
                    if failState is None:
                        continue
                    self.data_offload(failState)
                case "2" | "retrieve":
                    failState = self._get_bool_input("Enter fail state for retrieval (true/false): ")
                    if failState is None:
                        continue
                    self.data_retrieve(failState)
                case "3" | "db_pinger":
                    self.db_pinger()
                case "4" | "mallory_attempt":
                    self.mallory_attempt()
                case "5" | "display_server":
                    self.display_server_state()
                case "6" | "set_state":
                    state = self._get_bool_input("Enter fail state for operations (true/false): ")
                    if state is None:
                        continue
                    self.set_fail_state(state)
                case "7" | "set_display":
                    mode = self._get_bool_input("Enter display mode (true/false): ")
                    if mode is None:
                        continue
                    self.set_display_mode(mode)
                case "8" | "fail_example":
                    self.fail_example()
                case "9" | "success_example":
                    self.success_example()
                case "10" | "full_display":
                    self.full_display()
                case "11" | "exit":
                    print("Exiting...")
                    break
                case "12" | "reset":
                    self.reset_system()
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

        if self.server.displayMode:
            print(f"Eve sees data: {data} and signature: {signature.hex()}")
        
        if success:
            print("Data retrieval successful with failstate: ", state)
        else:
            print("Data retrieval failed with failstate: ", state)
    
    """
    Tests the database connectivity by performing multiple mockup CRUD operations.
    """
    def db_pinger(self):
        for i in range(10):
            if self.server.crud_mockup():
                print("Database operation successful.")
            else:
                print(f"Database operation failed after {i+1} attempts.")
                break
    
    """
    Simulates an interception and modification attack by an adversary (Mallory).
    """
    def mallory_attempt(self):
        print("Mallory is attempting to intercept and modify data...")
        data = "Mallory's malicious data"
        signature = b"invalid_signature"
        success = self.server.retrieve((data, signature))
        if not success:
            print("Mallory's attempt to modify data was detected and prevented.")
        else:
            print("Mallory has modified the data!")

    """
    Sets the display mode for the connection, server, and client.
    
    @param mode: Boolean to enable or disable verbose output.
    """
    def set_display_mode(self, mode):
        self.displayMode = mode
        self.server.displayMode = mode
        self.client.displayMode = mode

    """
    Sets the fail state for both the server and the client to simulate system failures.
    
    @param state: Boolean indicating the desired fail state.
    """
    def set_fail_state(self, state):
        self.server.failState = state
        self.client.failState = state

    """
    Triggers the server to display its current internal state.
    """
    def display_server_state(self):
        self.server.display_server_internal_state()

    """
    Executes a sequence of operations designed to demonstrate system behavior during failures.
    """
    def fail_example(self):
        print("\nSimulating a failure in the system...")
        self.set_fail_state(True)
        self.data_offload(state=False)
        self.data_retrieve(state=True)
        self.db_pinger()
        self.mallory_attempt()
        self.display_server_state()
        self.set_fail_state(False)
    
    """
    Executes a sequence of operations designed to demonstrate a successful system flow.
    """
    def success_example(self):
        print("\nSimulating a successful operation in the system...")
        self.set_fail_state(False)
        self.data_offload(state=False)
        self.data_retrieve(state=False)
        self.db_pinger()
        self.mallory_attempt()
        self.display_server_state()

    """
    Runs both the success and failure examples with verbose output enabled.
    """
    def full_display(self):
        self.set_display_mode(True)
        self.success_example()
        self.fail_example()
        
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
        
    """
    Resets the entire system (both server and client) to its default state.
    """
    def reset_system(self):
        self.server.reset_server_state()
        self.client.reset_client_state()
        print("System state has been reset to default values.")

start = Connection()

start.command_line()

    
