from pathlib import Path

# Accept request from all network interfaces ( 0.0.0.0 )
# Server Binding address
SERVER_HOST = "0.0.0.0"

# Define Host and Port of the sender target address
CLIENT_HOST = "127.0.0.1"
PORT = 5000

# File needed to be transferred
TRANSFER_DIR = Path("transfer")
RECIEVED_DIR = Path("recieved")
LOG_FILE = "logs/bebop.log"

CHUNK_SIZE = 1024

CHECKPOINT_INTERVAL = 1024 * 1024

DISCOVERY_PORT = 5001
DISCOVERY_MESSAGE = "BEBOP_DISCOVER"
DISCOVERY_RESPONSE = "BEBOP_RESPONSE"


TRANSFER_REQUEST = "TRANSFER_REQUEST"
TRANSFER_ACCEPT = "TRANSFER_ACCEPT"
TRANSFER_REJECT = "TRANSFER_REJECT"
