from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

# Accept request from all network interfaces ( 0.0.0.0 )
# Server Binding address
SERVER_HOST = "0.0.0.0"

# Define Host and Port of the sender target address
CLIENT_HOST = "127.0.0.1"
PORT = 5000

# File needed to be transferred
TRANSFER_DIR = DATA_DIR / "shared"
RECIEVED_DIR = DATA_DIR / "recieved"
LOG_FILE = DATA_DIR / "bebop.log"
DB_PATH = DATA_DIR / "bebop.db"

CHUNK_SIZE = 1024

CHECKPOINT_INTERVAL = 1024 * 1024

DISCOVERY_PORT = 5001
DISCOVERY_MESSAGE = "BEBOP_DISCOVER"
DISCOVERY_RESPONSE = "BEBOP_RESPONSE"


TRANSFER_REQUEST = "TRANSFER_REQUEST"
TRANSFER_ACCEPT = "TRANSFER_ACCEPT"
TRANSFER_REJECT = "TRANSFER_REJECT"
