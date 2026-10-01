from pathlib import Path

from docx import Document


def load_docx(file_path: Path) -> str:

    document = Document(
        str(file_path)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(
                text
            )

    return "\n\n".join(
        paragraphs
    )