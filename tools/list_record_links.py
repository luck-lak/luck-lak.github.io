from __future__ import annotations

import re
import sys

from docx import Document

from build_learning_records import DOCX_PATH, RECORD_STARTS, normalize_text


def paragraph_hyperlinks(paragraph, document) -> list[dict]:
    links = []
    for hyperlink in paragraph._p.xpath(".//w:hyperlink"):
        relationship_ids = hyperlink.xpath("@r:id")
        if not relationship_ids:
            continue
        text = "".join(hyperlink.xpath(".//w:t/text()"))
        relationship = document.part.rels[relationship_ids[0]]
        links.append({"text": text, "url": relationship.target_ref})
    return links


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    document = Document(DOCX_PATH)
    paragraphs = document.paragraphs
    boundaries = []
    for index, paragraph in enumerate(paragraphs):
        text = normalize_text(paragraph.text)
        for number, expected_start in RECORD_STARTS.items():
            if text.startswith(expected_start):
                boundaries.append((number, index))
                break

    boundaries.sort()
    for position, (number, start) in enumerate(boundaries):
        end = boundaries[position + 1][1] if position + 1 < len(boundaries) else len(paragraphs)
        links = []
        for paragraph in paragraphs[start:end]:
            links.extend(paragraph_hyperlinks(paragraph, document))

        print(f"Record {number:02d}")
        for link in links:
            print(f"  {link['url']} | {link['text']}")


if __name__ == "__main__":
    main()
