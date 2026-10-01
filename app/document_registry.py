import hashlib
import json
from pathlib import Path


REGISTRY_PATH = Path(
    "data/document_registry.json"
)


def calculate_file_hash(
    file_path: Path
) -> str:

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def load_registry():

    if not REGISTRY_PATH.exists():
        return {}

    with REGISTRY_PATH.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_registry(registry):

    REGISTRY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with REGISTRY_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )


def is_document_changed(
    file_path: Path,
    registry
):

    current_hash = calculate_file_hash(
        file_path
    )

    filename = file_path.name

    previous = registry.get(
        filename
    )

    if previous is None:
        return True, current_hash

    if previous.get("hash") != current_hash:
        return True, current_hash

    return False, current_hash