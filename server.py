from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

"""
Represents the server node responsible for data preparation, signing, and integrity verification.
"""
class Server:

    """
    Initializes the server with default data, cryptographic keys, and an empty hash cache.
    """
    def __init__(self):
        self.name = "server"
        self.dataCache = "I love security!"
        self.hashCache = None
        self.failState = False
        self.private_key, self.public_key = self.generate_rsa_keys()
        self.client_public_key = None

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
    Stores the client's public key for signature verification.
    
    @param client_public_key: The RSA public key of the client.
    """
    def set_client_public_key(self, client_public_key):
        self.client_public_key = client_public_key
        print(f"{self.name} received client's public key.")
    
    """
    @return: The stored client public key.
    """
    def get_client_public_key(self):
        return self.client_public_key
    
    """
    Signs the provided data using the server's private key and SHA-256.
    
    @param data: The string data to sign.
    @return: The generated digital signature.
    """
    def generate_signature(self, data):
        print(f"{self.name} generating signature for data: {data}")

        
        # Sign the raw data bytes directly using the private key
        signature = self.private_key.sign(
            data.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        print("Signature generated")
        return signature
    
    """
    Verifies the signature of the provided data using the client's public key.
    
    @param data: The signed string data.
    @param signature: The digital signature to verify.
    @return: True if verification is successful, False otherwise.
    """
    def verify_signature(self, data, signature):
        try:
            self.client_public_key.verify(
                signature,
                data.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print(f"{self.name} signature verification successful.")
            return True
        except Exception:
            print(f"{self.name} signature verification failed.")
            return False

    """
    Sets the internal data cache.
    
    @param data: The new data string.
    """
    def set_data(self, data):
        self.dataCache = data

    """
    Computes a SHA-256 hash of the provided data.
    
    @param data: The data to hash.
    @return: The hexadecimal representation of the hash.
    """
    def compute_hash(self, data):
        print(f"Computing hash of data: {data}")
        digest = hashes.Hash(hashes.SHA256())
        digest.update(str(data).encode())
        result = digest.finalize().hex()
        print(f"Hash computed: {result}")
        return result

    """
    Verifies the provided data against the stored hash cache.
    
    @param data: The data to verify.
    @return: True if the hash matches, False otherwise.
    """
    def verify_hash(self, data):
        print(f"Verifying hash of data: {data}")
        if self.hashCache == self.compute_hash(data):
            print("Hash verification successful!")
            return True
        else:
            print("Hash verification failed!")
            return False
            
    """
    Prepares data for offloading by hashing it and generating a digital signature.
    
    @return: A tuple containing (data, signature).
    """
    def offload(self):
        print(f"Data to offload: {self.dataCache}")
        
        data = self.dataCache

        self.hashCache = self.compute_hash(data)
        signature = self.generate_signature(data)
        print("Offloading data to connection...")
        self.dataCache = None
        return data, signature

    """
    Retrieves data from a packet and verifies its integrity and signature.
    
    @param data_packet: A tuple containing (data, signature).
    @return: True if retrieval and verification are successful, False otherwise.
    """
    def retrieve(self, data_packet):
        data, signature = data_packet
        print("Retrieving data from connection...")

        if not self.verify_signature(data, signature) and not self.failState:
            return False   
        elif not self.failState:
            if self.verify_hash(data):
                self.dataCache = data
                print(f"Data retrieved successfully. Current data cache: {self.dataCache}")
                return True
            else:
                print(f"Failed to retrieve data. Current data cache: {self.dataCache}")
                return False
        else:
            self.dataCache = data
            print(f"Data retrieved successfully. Current data cache: {self.dataCache}")
            return True
