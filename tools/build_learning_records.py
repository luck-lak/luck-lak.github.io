from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path
import re
import sys

from docx import Document
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "学习探索记录.docx"
RECORDS_DIR = ROOT / "records"
ASSETS_DIR = ROOT / "assets" / "records"


RECORD_TITLES = {
    1: "AI Agents in LangGraph",
    2: "Long-Term Agentic Memory with LangGraph",
    3: "Building toward Computer Use with Anthropic",
    4: "Evaluating AI Agents",
    5: "Pretraining LLMs",
    6: "Post-training of LLMs",
    7: "Reinforcement Fine-Tuning LLMs with GRPO",
    8: "Transformers in Practice",
    9: "Agent Skills with Anthropic",
    10: "Paper: Trustworthy LLM Agents",
    11: "Paper: Agent Skill Evaluation and Evolution",
    12: "Building Code Agents with Hugging Face smolagents",
    13: "Fast LLM Inference with Cerebras",
    14: "Fast & Efficient LLM Inference with vLLM",
    15: "How Diffusion Models Work",
}

RECORD_STARTS = {
    1: "1.AI Agents In LangGraph",
    2: "2.Long-Term Agentic Memory With LangGraph",
    3: "3.Building toward Computer Use with Anthropic",
    4: "4.Evaluating AI Agents",
    5: "5.Pretraining LLMs",
    6: "6.Post-training of LLMs",
    7: "7.Reinforcement Fine-Tuning LLMs With GRPO",
    8: "8.Transformers in Practice",
    9: "9.Agent Skills with Anthropic",
    10: "10.论文",
    11: "11.论文",
    12: "12.Building Code Agents with Hugging Face smolagents",
    13: "13.Fast LLM Inference with Cerebras",
    14: "14.Fast & Efficient LLM Inference with vLLM",
    15: "15.How Diffusion Models Work",
}

RECORD_COVER_EXTENSIONS = {10: "svg", 11: "svg"}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def paragraph_image_ids(paragraph) -> list[str]:
    return paragraph._p.xpath(".//a:blip/@r:embed")


def save_image(image_part, output_path: Path, max_size: int, quality: int) -> None:
    with Image.open(BytesIO(image_part.blob)) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode in {"RGBA", "LA", "P"}:
            image = image.convert("RGBA")
            background = Image.new("RGBA", image.size, "white")
            image = Image.alpha_composite(background, image).convert("RGB")
        else:
            image = image.convert("RGB")
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)


def build_record_pages(document: Document) -> list[dict]:
    paragraphs = document.paragraphs
    boundaries: list[int] = []
    for index, paragraph in enumerate(paragraphs):
        text = normalize_text(paragraph.text)
        for number, expected_start in RECORD_STARTS.items():
            if text.startswith(expected_start):
                boundaries.append(index)
                break

    boundaries.sort()
    records: list[dict] = []

    for position, start in enumerate(boundaries):
        end = boundaries[position + 1] if position + 1 < len(boundaries) else len(paragraphs)
        number = position + 1
        title = RECORD_TITLES[number]
        slug = f"{number:02d}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}"
        record_dir = ASSETS_DIR / slug
        page_path = RECORDS_DIR / f"{slug}.html"

        content_blocks: list[str] = []
        image_count = 0
        first_image_path: Path | None = None

        for paragraph in paragraphs[start + 1 : end]:
            text = normalize_text(paragraph.text)
            image_ids = paragraph_image_ids(paragraph)

            for image_id in image_ids:
                image_part = document.part.related_parts[image_id]
                image_count += 1
                image_name = f"{image_count:02d}.jpg"
                image_path = record_dir / image_name
                save_image(image_part, image_path, max_size=1400, quality=82)
                relative_image_path = f"../assets/records/{slug}/{image_name}"
                content_blocks.append(
                    f'<figure class="record-figure"><img src="{relative_image_path}" alt="Course screenshot" loading="lazy"></figure>'
                )
                if first_image_path is None:
                    first_image_path = image_path

            if text:
                if re.fullmatch(r".{0,30}：", text):
                    content_blocks.append(f"<h3>{escape(text[:-1])}</h3>")
                else:
                    content_blocks.append(f"<p>{escape(text)}</p>")

        if first_image_path is not None:
            thumbnail_path = ASSETS_DIR / "thumbnails" / f"{number:02d}.jpg"
            save_image_from_path(first_image_path, thumbnail_path, max_size=720, quality=80)
        else:
            thumbnail_path = None

        records.append(
            {
                "number": number,
                "title": title,
                "slug": slug,
                "page_path": page_path,
                "thumbnail_path": thumbnail_path,
                "content": "\n".join(content_blocks),
            }
        )

    return records


def save_image_from_path(source: Path, output_path: Path, max_size: int, quality: int) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode in {"RGBA", "LA", "P"}:
            image = image.convert("RGBA")
            background = Image.new("RGBA", image.size, "white")
            image = Image.alpha_composite(background, image).convert("RGB")
        else:
            image = image.convert("RGB")
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)


def render_record_page(record: dict, previous_record: dict | None, next_record: dict | None) -> str:
    previous_link = ""
    next_link = ""
    if previous_record:
        previous_link = f'<a class="record-pagination-link previous" href="{previous_record["slug"]}.html">Previous</a>'
    if next_record:
        next_link = f'<a class="record-pagination-link next" href="{next_record["slug"]}.html">Next</a>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escape(record["title"])} learning record by Aokun Lei.">
    <title>{escape(record["title"])} | Aokun Lei</title>
    <link rel="icon" href="../assets/images/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../css/style.css">
    <script src="../js/main.js" defer></script>
</head>
<body>
    <header>
        <a class="site-title" href="../index.html">AOKUN</a>
        <nav class="main-navigation">
            <a href="../index.html">Home</a>
            <a href="../learning-records.html" class="active">Learning Records</a>
        </nav>
        <button class="theme-button" type="button">🌙</button>
    </header>

    <main class="record-page">
        <article class="record-article">
            <p class="record-kicker">Learning Record {record["number"]:02d}</p>
            <h1>{escape(record["title"])}</h1>
            <div class="record-content">
{record["content"]}
            </div>
            <nav class="record-pagination">
                {previous_link}
                <a class="record-pagination-link index" href="../learning/deeplearning-ai.html">All DeepLearning.AI records</a>
                {next_link}
            </nav>
        </article>
    </main>

    <footer>
        <p>© 2026 AOKUN LEI</p>
    </footer>
</body>
</html>
'''


def render_index_page(records: list[dict]) -> str:
    cards = []
    for record in records:
        thumbnail = ""
        if record["thumbnail_path"] is not None:
            extension = RECORD_COVER_EXTENSIONS.get(record["number"], "jpg")
            thumbnail_relative = f"../assets/records/thumbnails/{record['number']:02d}.{extension}"
            thumbnail = f'<img src="{thumbnail_relative}" alt="{escape(record["title"])} cover image" loading="lazy">'
        cards.append(
            f'''<a class="record-card" href="../records/{record["slug"]}.html">
                {thumbnail}
                <div class="record-card-text">
                    <p class="record-card-number">Record {record["number"]:02d}</p>
                    <h2>{escape(record["title"])}</h2>
                </div>
            </a>'''
        )

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Aokun Lei's learning records from DeepLearning.AI courses and paper notes.">
    <title>Learning Records | Aokun Lei</title>
    <link rel="icon" href="../assets/images/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../css/style.css">
    <script src="../js/main.js" defer></script>
</head>
<body>
    <header>
        <a class="site-title" href="../index.html">AOKUN</a>
        <nav class="main-navigation">
            <a href="../index.html">Home</a>
            <a href="../index.html#projects">Projects</a>
            <a href="../index.html#technical-journey">Technical Journey</a>
            <a href="./learning-records.html" class="active">Learning Records</a>
        </nav>
        <button class="theme-button" type="button">🌙</button>
    </header>

    <main class="records-index-page">
        <section class="records-intro">
            <p class="records-platform">Platform: DeepLearning.AI</p>
            <h1>DeepLearning.AI Records</h1>
            <p>Notes from DeepLearning.AI short courses and paper reading. Each record keeps the original wording and screenshots from my DOCX notebook, so the records read best as a map of what each course covers.</p>
            <a class="download-link" href="../学习探索记录.docx" download>Download the original DOCX</a>
            <p class="platform-backlink"><a href="../learning-records.html">← All learning records</a></p>
        </section>

        <section class="record-grid">
            {"".join(cards)}
        </section>
    </main>

    <footer>
        <p>© 2026 AOKUN LEI</p>
    </footer>
</body>
</html>
'''


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    document = Document(DOCX_PATH)
    records = build_record_pages(document)

    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    for index, record in enumerate(records):
        previous_record = records[index - 1] if index > 0 else None
        next_record = records[index + 1] if index + 1 < len(records) else None
        record["page_path"].write_text(render_record_page(record, previous_record, next_record), encoding="utf-8")

    index_path = ROOT / "learning" / "deeplearning-ai.html"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(render_index_page(records), encoding="utf-8")

    print(f"Generated {len(records)} record pages and 1 index page.")


if __name__ == "__main__":
    main()
