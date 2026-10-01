from pathlib import Path


def load_txt(file_path: Path):

    text = file_path.read_text(
        encoding="utf-8"
    )

    return [
        {
            "text": text,
            "page": None
        }
    ]