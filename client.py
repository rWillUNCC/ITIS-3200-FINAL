from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

"""
Represents the client node responsible for receiving, storing, and sending data back to the server.
"""
class Client:
    """
    Initializes the client with RSA keys and an empty data cache.
    """
    def __init__(self):
        self.name = "client"
        self.dataCache = ""
        self.private_key, self.public_key = self.generate_rsa_keys()
        self.server_public_key = None
        self.failState = False
        self.displayMode = True

    
    """
    Generates a new pair of RSA keys (2048-bit).
    
    @return: A tuple containing (private_key, public_key).
    """
    def generate_rsa_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    """
    Stores the server's public key for signature verification.
    
    @param server_public_key: The RSA public key of the server.
    """
    def set_server_public_key(self, server_public_key):
        self.server_public_key = server_public_key
    
    """
    @return: The stored server public key.
    """
    def get_server_public_key(self):
        return self.server_public_key

    """
    Signs the provided data using the client's private key and SHA-256.
    
    @param data: The string data to sign.
    @return: The generated digital signature.
    """
    def generate_signature(self, data):
        if self.displayMode:
            print(f"{self.name} generating signature for data: {data}")
            
        signature = self.private_key.sign(
            data.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        if self.displayMode:
            print("Signature generated")
        return signature

    """
    Verifies the signature of the provided data using the server's public key.
    
    @param data: The signed string data.
    @param signature: The digital signature to verify.
    @return: True if verification is successful, False otherwise.
    """
    def verify_signature(self, data, signature):
        try:
            self.server_public_key.verify(
                signature,
                data.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print(f"{self.name} signature verification successful.")
            return True
        except (InvalidSignature, TypeError):
            print(f"{self.name} signature verification failed.")
            return False
    
    """
    Receives data from the server, verifies its signature, and stores it.
    
    @param failState: Boolean indicating if a failure should be simulated.
    @param data_packet: A tuple containing (data, signature).
    @return: True if data is received and verified, False otherwise.
    """
    def receive_data(self, failState, data_packet):
        data, signature = data_packet
        if failState:
            print(f"{self.name} simulated a failure during reception.")
            return False

        if self.verify_signature(data, signature):
            print(f"{self.name} received and verified data: {data}")
            self.dataCache = data
            return True
        return False

    """
    Prepares data to be sent back to the server, optionally simulating corruption.
    
    @param failState: Boolean indicating if corrupted data should be sent.
    @return: A tuple containing (data, signature).
    """
    def send_data(self, failState):
        if self.displayMode:
            print(f"{self.name} sending data...")
        data = "I hate security!" if failState else self.dataCache
        signature = self.generate_signature(data)
        return data, signature
        
    """
    Resets the client's internal state to its initial default values.
    """
    def reset_client_state(self):
        self.dataCache = ""
        self.failState = False
        self.displayMode = True