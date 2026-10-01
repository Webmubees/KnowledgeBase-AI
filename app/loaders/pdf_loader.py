from pathlib import Path

from pypdf import PdfReader


def load_pdf(file_path: Path):

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:
            pages.append(
                {
                    "text": text,
                    "page": page_number
                }
            )

    return pages