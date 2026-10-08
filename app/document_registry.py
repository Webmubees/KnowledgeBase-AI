import json
import hashlib
from pathlib import Path


REGISTRY_PATH = Path("chroma_db/document_registry.json")


def calculate_hash(file_path):

    hasher = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def load_registry():

    if not REGISTRY_PATH.exists():
        return {}

    with open(
        REGISTRY_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_registry(registry):

    REGISTRY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REGISTRY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )


def get_file_status(
    file_path,
    registry
):

    filename = file_path.name

    if filename not in registry:
        return "new"

    current_hash = calculate_hash(
        file_path
    )

    if registry[filename]["hash"] != current_hash:
        return "modified"

    return "unchanged"


def update_registry(
    file_path,
    registry
):

    registry[file_path.name] = {
        "hash": calculate_hash(file_path)
    }


def remove_from_registry(
    filename,
    registry
):

    if filename in registry:

        del registry[filename]