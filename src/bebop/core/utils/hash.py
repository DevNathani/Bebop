import hashlib
from pathlib import Path


def calculate_sha256(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as file:
        while chunk := file.read(1024):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()
