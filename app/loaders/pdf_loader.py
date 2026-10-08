from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: Path) -> list[dict]:
    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages