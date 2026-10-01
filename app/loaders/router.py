from pathlib import Path

from loaders.txt_loader import load_txt
from loaders.pdf_loader import load_pdf
from loaders.docx_loader import load_docx


def load_file(file_path: Path):

    extension = file_path.suffix.lower()

    if extension == ".txt":
        return load_txt(file_path)

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )