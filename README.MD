# Secure Data Offloading Simulation

This project simulates a secure communication channel between a **Server** and a **Client**, focusing on data integrity and authenticity. It demonstrates how cryptographic primitives like RSA signatures and SHA-256 hashing protect data during offloading and retrieval.

## Prerequisites

- Python 3.10 or higher
- `cryptography` library

To install the required library, run:
```bash
pip install -r requirements.txt
```

## How to Run

To start the system and access the command-line interface, execute:
```bash
python connection.py
```

## 1. Secure System (Success Case)

To observe the system functioning correctly under secure protocols:

*   **Automated Demo:** Enter `9` or `success_example`. This performs a full cycle: offloading data, retrieving it, checking database health, and verifying that an external attack is blocked.
*   **Manual Step-by-Step:**
    1.  Enter `offload` and type `false` when prompted for a fail state.
    2.  Enter `retrieve` and type `false` when prompted for a fail state.
    3.  Enter `db_pinger`.
    3.  The console will show that signatures were verified and hashes matched. It will also showcase the rate limiter.

## 2. Attack or Misuse (Failure Case)

To test the system's resilience and see security checks in action:
*   **Failure Case Switch:** Enter `6` or `set_state` and type `true`. This toggles the internal `failState` for both nodes, causing the system to bypass RSA signature and SHA-256 hash verifications, simulating a compromised internal environment.
*   **Automated Demo:** Enter `8` or `fail_example`. This forces the system into various error states to show how it handles corrupted data or failed transfers.
*   **Simulate Mallory (Interception):** Enter `4` or `mallory_attempt`. This simulates an attacker injecting malicious data with an invalid signature. The server will detect this and reject the data.
*   **Data Corruption:** Enter `retrieve` and type `true` when prompted for a fail state. The client will intentionally send altered data, causing the server's hash verification to fail.
*

## Mechanism and Attack Implementation

### Security Mechanisms
*   **RSA Digital Signatures:** During initialization, both nodes generate 2048-bit RSA keys and exchange public keys. Every data transfer is signed by the sender's private key. The receiver uses the sender's public key to verify that the message actually came from the trusted source.
*   **SHA-256 Integrity Hashing:** Before offloading, the Server computes a SHA-256 hash of the data and stores it in a `hashCache`. Upon retrieval, the Server re-hashes the incoming data. If the hashes don't match, the system knows the data was tampered with or corrupted.
*   **Rate Limiting (DB Gate):** The Server includes a `db_gate` that limits database operations to 5 requests per 60 seconds, simulating a basic defense against overprovisioning.

### Attack and Failure Simulation
*   **Mallory's Interception:** This is implemented by bypassing the standard Client logic. The `Connection` class directly feeds the Server's `retrieve` method with a string labeled "Mallory's malicious data" and a dummy signature `b"invalid_signature"`.
*   **Fail State Logic:** The `failState` flags in the `Client` and `Server` classes allow the simulation of internal errors. For example, when the Client's `send_data` is called with a fail state, it intentionally replaces the cached data with the string `"I hate security!"`, which triggers a verification failure at the Server.
*   **Signature Exceptions:** The system uses the `cryptography` library's `InvalidSignature` exception handling to catch and report unauthorized modifications during the RSA verification process.

### CLI Descriptions

| Command | Alternative | Description |
| :--- | :--- | :--- |
| `1` | `offload` | Initiates data offloading from the Server to the Client with signing. |
| `2` | `retrieve` | Triggers the retrieval process to verify data integrity and signatures. |
| `3` | `db_pinger` | Demonstrates the rate-limiting (DB Gate) mechanism. |
| `4` | `mallory_attempt` | Simulates an external actor injecting malicious data. |
| `5` | `display_server` | Outputs the current internal state of the Server node. |
| `6` | `set_state` | Toggles the failure state for simulated system components. |
| `7` | `set_display` | Toggles verbose logging for cryptographic operations. |
| `8` | `fail_example` | Runs an automated sequence showing various failure/attack states. |
| `9` | `success_example` | Runs an automated sequence showing a successful data lifecycle. |
| `10` | `full_display` | Executes both success and failure examples in succession. |
| `11` | `exit` | Safely terminates the simulation. |
| `12` | `reset` | Resets the Server and Client caches and counters to defaults. |
