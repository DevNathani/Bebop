import logging

from bebop.config.config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,  # file destination
    level=logging.INFO,
    format=("%(asctime)s | %(levelname)s | %(message)s"),
)

logger = logging.getLogger("bebop")
