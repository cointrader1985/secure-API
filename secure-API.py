# API-driven contract signing system using endpoints and API key authentication
import hashlib
import json
import uuid
import time
from datetime import datetime

class ServerConfig:
    def __init__(self, api_key):
        self.api_key = api_key
        self.created = time.time()

class Contract:
    def __init__(self, user, resource, action):
        self.id = str(uuid.uuid4())
        self.user = user
        self.resource = resource
        self.action = action
        self.created = time.time()
        self.approved = False
        self.signature = None

    def serialize(self):
        return json.dumps({
            "id": self.id,
            "user": self.user,
            "resource": self.resource,
            "action": self.action,
            "approved": self.approved,
            "created": self.created
        }, sort_keys=True)

    def hash(self):
        return hashlib.sha256(self.serialize().encode()).hexdigest()

    def approve(self):
        self.approved = True

    def sign(self, key):
        base = self.hash()
        self.signature = hashlib.sha256(f"{base}:{key}".encode()).hexdigest()
        return self.signature

    def verify(self, key):
        expected = hashlib.sha256(f"{self.hash()}:{key}".encode()).hexdigest()
        return expected == self.signature

def endpoint_create(user, resource, action, config):
    if not config.api_key:
        raise Exception("Missing API key")
    return Contract(user, resource, action)

def endpoint_approve(contract):
    contract.approve()
    return contract

def endpoint_sign(contract, config):
    if not contract.approved:
        raise Exception("Contract not approved")
    return contract.sign(config.api_key)

def endpoint_verify(contract, config):
    return contract.verify(config.api_key)

def simulate_server():
    config = ServerConfig("secure_api_key_123")

    contract = endpoint_create("Alice", "StorageBucket", "WRITE")
    contract = endpoint_approve(contract)
    signature = endpoint_sign(contract, config)

    print("Contract ID:", contract.id)
    print("Approved:", contract.approved)
    print("Signature:", signature)
    print("Valid:", endpoint_verify(contract, config))

    return contract

def audit(contract):
    print("\nAudit Log")
    print(contract.serialize())

def summary():
    print("\nServer configuration active")

def main():
    contract = simulate_server()
    audit(contract)
    summary()
    print("Finished execution")

if __name__ == "__main__":
    main()
