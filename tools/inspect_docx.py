from pathlib import Path
import sys

from docx import Document


DOCX_PATH = Path(__file__).resolve().parents[1] / "学习探索记录.docx"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    document = Document(DOCX_PATH)
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        image_ids = paragraph._p.xpath(".//a:blip/@r:embed")
        if 320 <= index <= 375:
            preview = text.replace("\n", " ")[:180]
            print(f"{index:04d} | style={paragraph.style.name!r} | images={image_ids} | {preview}")


if __name__ == "__main__":
    main()
