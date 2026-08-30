from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path
import re

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.hyperlink import Hyperlink
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT.parent / "codecademy"
RECORDS_OUTPUT_DIR = ROOT / "records" / "codecademy"
ASSETS_DIR = ROOT / "assets" / "records" / "codecademy"
THUMBNAILS_DIR = ROOT / "assets" / "records" / "thumbnails" / "codecademy"
PLATFORM_PAGE = ROOT / "learning" / "codecademy.html"

PLATFORM_INTRO = (
    "Notes from Codecademy courses on web development and computer science "
    "fundamentals. Like my other records, these keep the original wording and "
    "screenshots from my notebook, so they work best as a map of what each "
    "course covers."
)

# One entry per course. "kind" chooses how the document is split:
#   chapters   - split on 第X章章节总结（Topic） markers
#   flat       - one flowing section, headings and tables stay inline
#   cheatsheet - split on exact "cheat_headings" lines, render code and tables
#   markdown   - split on "# " headings in a Markdown file
RECORDS = [
    {
        "file": "frontend/Learn HTML.docx",
        "title": "Learn HTML",
        "slug": "learn-html",
        "kind": "chapters",
    },
    {
        "file": "frontend/Learn CSS.docx",
        "title": "Learn CSS",
        "slug": "learn-css",
        "kind": "chapters",
    },
    {
        "file": "frontend/CSS intermidiate.docx",
        "title": "Intermediate CSS",
        "slug": "intermediate-css",
        "kind": "chapters",
    },
    {
        "file": "frontend/Building Interactive JavaScript Websites.docx",
        "title": "Building Interactive JavaScript Websites",
        "slug": "building-interactive-javascript-websites",
        "kind": "chapters",
    },
    {
        "file": "backend/what is backend.md",
        "title": "Introduction to Back-End Programming",
        "slug": "introduction-to-back-end-programming",
        "kind": "markdown",
    },
    {
        "file": "backend/Learn Node.js--Fundmentals.docx",
        "title": "Learn Node.js: Fundamentals",
        "slug": "learn-node-js-fundamentals",
        "kind": "chapters",
    },
    {
        "file": "backend/Learn Node.js Setting Up a Server.docx",
        "title": "Learn Node.js: Setting Up a Server",
        "slug": "learn-node-js-setting-up-a-server",
        "kind": "flat",
    },
    {
        "file": "Fundermentals of Operating Systems.docx",
        "title": "Fundamentals of Operating Systems",
        "slug": "fundamentals-of-operating-systems",
        "kind": "chapters",
    },
    {
        "file": "cloud computing .docx",
        "title": "Cloud Computing",
        "slug": "cloud-computing",
        "kind": "flat",
    },
    {
        "file": "git.docx",
        "title": "Git: Team Collaboration Cheat Sheet",
        "slug": "git-team-collaboration",
        "kind": "cheatsheet",
        "cheat_headings": ["前置准备（仅首次）", "9步流程", "命令速查", "核心概念", "口诀"],
        "code_prefixes": ["git "],
    },
    {
        "file": "Learn the  Command Line.docx",
        "title": "Learn the Command Line",
        "slug": "learn-the-command-line",
        "kind": "chapters",
    },
]

CHAPTER_PATTERN = re.compile(r"^第([一二三四五六七八九十\d]+)章+章节总结(?:[（(](.+?)[)）])?\s*$")
CHAPTER_NUMBERS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
SITE_LINK_PATTERN = re.compile(r"^网站[:：]")
MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def iter_blocks(document: Document):
    """Yield paragraphs and tables in true document order."""
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def inline_html(paragraph: Paragraph) -> str:
    """Render a paragraph, keeping hyperlinks and line breaks alive."""
    parts = []
    for item in paragraph.iter_inner_content():
        if isinstance(item, Hyperlink):
            url = escape(item.url or "", quote=True)
            parts.append(
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">{escape(item.text)}</a>'
            )
        else:
            parts.append(escape(item.text))
    return "".join(parts).replace("\n", "<br>")


def paragraph_text(paragraph: Paragraph) -> str:
    return paragraph.text.strip()


def is_label_line(text: str) -> bool:
    """Short lines that end with a colon behave like small headings."""
    return len(text) <= 60 and text.endswith(("：", ":"))


def chapter_heading(text: str) -> tuple[int, str] | None:
    match = CHAPTER_PATTERN.match(text)
    if match is None:
        return None
    raw_number = match.group(1)
    number = CHAPTER_NUMBERS.get(raw_number)
    if number is None:
        number = int(raw_number)
    return number, (match.group(2) or "").strip()


def save_image(image_part, output_path: Path) -> None:
    with Image.open(BytesIO(image_part.blob)) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode in {"RGBA", "LA", "P"}:
            image = image.convert("RGBA")
            background = Image.new("RGBA", image.size, "white")
            image = Image.alpha_composite(background, image).convert("RGB")
        else:
            image = image.convert("RGB")
        image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "JPEG", quality=82, optimize=True, progressive=True)


def save_images(paragraph: Paragraph, record_dir: Path, counter: list[int], html: list[str]) -> None:
    for image_id in paragraph._p.xpath(".//a:blip/@r:embed"):
        counter[0] += 1
        image_name = f"{counter[0]:02d}.jpg"
        save_image(paragraph.part.related_parts[image_id], record_dir / image_name)
        html.append(
            f'<figure class="record-figure"><img src="../../assets/records/codecademy/{record_dir.name}/{image_name}" '
            'alt="Course screenshot" loading="lazy"></figure>'
        )


def table_html(table: Table) -> str:
    rows = []
    for row in table.rows:
        cells = [escape(cell.text.strip()).replace("\n", "<br>") for cell in row.cells]
        rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    return '<table class="record-table">' + "".join(rows) + "</table>"


def start_section(sections: list[dict], title: str) -> dict:
    section = {"title": title, "html": []}
    sections.append(section)
    return section


def build_docx_sections(record: dict, record_dir: Path) -> tuple[list[dict], str | None]:
    document = Document(SOURCE_DIR / record["file"])
    kind = record["kind"]
    sections: list[dict] = []
    used = {"section": None}
    image_counter = [0]
    source_url: str | None = None
    cheat = {"mode": None, "rows": [], "lines": []}
    list_buffer: list[str] = []
    main_started = False
    normalized_title = re.sub(r"\s+", " ", record["title"]).casefold()

    def default_title() -> str | None:
        return None if kind == "flat" else "Notes"

    def current_section() -> dict:
        if used["section"] is None:
            used["section"] = start_section(sections, default_title())
        return used["section"]

    def flush_cheat() -> None:
        """Write pending cheat-sheet rows or code lines in document order."""
        if cheat["mode"] == "table" and cheat["rows"]:
            rows = []
            for index, cells in enumerate(cheat["rows"]):
                tag = "th" if index == 0 else "td"
                cells_html = "".join(f"<{tag}>{cell}</{tag}>" for cell in cells)
                rows.append(f"<tr>{cells_html}</tr>")
            current_section()["html"].append('<table class="record-table">' + "".join(rows) + "</table>")
        elif cheat["mode"] == "code" and cheat["lines"]:
            code = "\n".join(cheat["lines"])
            current_section()["html"].append(f"<pre><code>{code}</code></pre>")
        cheat["mode"] = None
        cheat["rows"] = []
        cheat["lines"] = []

    def flush_list() -> None:
        """Keep consecutive Word list paragraphs together as one HTML list."""
        if list_buffer:
            items = "".join(f"<li>{item}</li>" for item in list_buffer)
            current_section()["html"].append(f"<ul>{items}</ul>")
            list_buffer.clear()

    def add_text(block: Paragraph, text: str, style: str) -> None:
        nonlocal source_url, main_started
        normalized_text = re.sub(r"\s+", " ", text).casefold()
        if normalized_text == normalized_title:
            return  # the document repeats the course title; the page header has it

        if SITE_LINK_PATTERN.match(text) and not main_started:
            if source_url is None:
                source_url = extract_source_url(block)
            return  # the course link moves to the page header

        if kind == "chapters":
            chapter = chapter_heading(text)
            if chapter is not None:
                flush_cheat()
                flush_list()
                main_started = True
                title = f"Chapter {chapter[0]}: {chapter[1]}" if chapter[1] else f"Chapter {chapter[0]}"
                used["section"] = start_section(sections, title)
                return

        if kind == "cheatsheet":
            if text in record.get("cheat_headings", []):
                flush_cheat()
                flush_list()
                main_started = True
                used["section"] = start_section(sections, text)
                return
            if "\t" in text:
                if cheat["mode"] != "table":
                    flush_cheat()
                    cheat["mode"] = "table"
                cheat["rows"].append([escape(cell.strip()) for cell in text.split("\t") if cell.strip()])
                return
            if any(text.startswith(prefix) for prefix in record.get("code_prefixes", [])):
                if cheat["mode"] != "code":
                    flush_cheat()
                    cheat["mode"] = "code"
                cheat["lines"].append(escape(text))
                return

        flush_cheat()
        section = current_section()
        if style == "List Paragraph":
            list_buffer.append(inline_html(block))
            return
        if style == "Heading 1":
            section["html"].append(f"<h2>{inline_html(block)}</h2>")
        elif style in {"Heading 2", "Heading 3"}:
            section["html"].append(f"<h3>{inline_html(block)}</h3>")
        elif is_label_line(text):
            section["html"].append(f"<h3>{inline_html(block)}</h3>")
        else:
            section["html"].append(f"<p>{inline_html(block)}</p>")

    for block in iter_blocks(document):
        if isinstance(block, Table):
            flush_cheat()
            flush_list()
            current_section()["html"].append(table_html(block))
            continue

        text = paragraph_text(block)

        if text and SITE_LINK_PATTERN.match(text) and not sections and source_url is None:
            source_url = extract_source_url(block)
            if kind == "chapters":
                continue  # the course link moves to the page header

        if block.style.name != "List Paragraph":
            flush_list()
        section = current_section()
        save_images(block, record_dir, image_counter, section["html"])
        if text:
            add_text(block, text, block.style.name)

    flush_cheat()
    flush_list()
    sections = [section for section in sections if section["html"]]
    return sections, source_url


def extract_source_url(paragraph: Paragraph) -> str | None:
    for item in paragraph.iter_inner_content():
        if isinstance(item, Hyperlink) and item.url:
            return item.url
    return None


def markdown_inline(text: str) -> str:
    escaped = escape(text)

    def replace_link(match: re.Match) -> str:
        label, url = match.group(1), escape(match.group(2), quote=True)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'

    return MD_LINK_PATTERN.sub(replace_link, escaped)


def build_markdown_sections(record: dict) -> tuple[list[dict], str | None]:
    lines = (SOURCE_DIR / record["file"]).read_text(encoding="utf-8").splitlines()
    sections: list[dict] = []
    source_url: str | None = None
    list_buffer: list[str] = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer and sections:
            items = "".join(f"<li>{markdown_inline(item)}</li>" for item in list_buffer)
            sections[-1]["html"].append(f"<ul>{items}</ul>")
        list_buffer = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_list()
            continue
        if set(line) <= set("-—"):
            flush_list()
            continue
        if line.startswith("# "):
            flush_list()
            sections.append({"title": line[2:].strip(), "html": []})
            continue
        if line.startswith("## "):
            text = line[3:].strip()
            link = re.match(r"^\[(.+?)\]\((.+?)\)$", text)
            if link and "网址" in link.group(1):
                source_url = link.group(2)
                continue
            flush_list()
            if len(text) > 80:  # long "headings" in this file are really paragraphs
                sections[-1]["html"].append(f"<p>{markdown_inline(text)}</p>")
            else:
                sections[-1]["html"].append(f"<h3>{markdown_inline(text)}</h3>")
            continue
        if line.startswith("### "):
            text = line[4:].strip()
            if text.startswith("- "):
                list_buffer.append(text[2:])
            else:
                flush_list()
                sections[-1]["html"].append(f"<h3>{markdown_inline(text)}</h3>")
            continue
        if line.startswith("- "):
            list_buffer.append(line[2:])
            continue
        flush_list()
        sections[-1]["html"].append(f"<p>{markdown_inline(line)}</p>")

    flush_list()
    sections = [section for section in sections if section["html"]]
    return sections, source_url


def render_sections(sections: list[dict]) -> str:
    blocks = []
    for index, section in enumerate(sections, start=1):
        title_html = f'<h2>{escape(section["title"])}</h2>' if section["title"] else ""
        blocks.append(
            f'<section class="record-section" id="section-{index}">\n'
            f"{title_html}\n"
            f'{"".join(section["html"])}\n'
            "</section>"
        )
    return "\n".join(blocks)


def render_toc(sections: list[dict]) -> str:
    titled = [(index, section) for index, section in enumerate(sections, start=1) if section["title"]]
    if len(titled) < 2:
        return ""
    items = "".join(
        f'<li><a href="#section-{index}">{escape(section["title"])}</a></li>'
        for index, section in titled
    )
    return f'<nav class="record-toc"><p class="record-toc-title">On this page</p><ul>{items}</ul></nav>'


def page_header(relative_root: str, active: str = "Learning Records") -> str:
    return f'''<header>
        <a class="site-title" href="{relative_root}index.html">AOKUN</a>
        <nav class="main-navigation">
            <a href="{relative_root}index.html">Home</a>
            <a href="{relative_root}index.html#projects">Projects</a>
            <a href="{relative_root}index.html#technical-journey">Technical Journey</a>
            <a href="{relative_root}learning-records.html" class="active">{active}</a>
        </nav>
        <button class="theme-button" type="button">🌙</button>
    </header>'''


def render_record_page(record: dict, number: int, previous: dict | None, next_record: dict | None, sections: list[dict], source_url: str | None) -> str:
    previous_link = ""
    next_link = ""
    if previous:
        previous_link = f'<a class="record-pagination-link previous" href="{previous["slug"]}.html">Previous</a>'
    if next_record:
        next_link = f'<a class="record-pagination-link next" href="{next_record["slug"]}.html">Next</a>'
    source_html = ""
    if source_url:
        url = escape(source_url, quote=True)
        source_html = f'<p class="record-source"><a href="{url}" target="_blank" rel="noopener noreferrer">Course page</a></p>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escape(record["title"])} learning record by Aokun Lei.">
    <title>{escape(record["title"])} | Aokun Lei</title>
    <link rel="icon" href="../../assets/images/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../../css/style.css">
    <script src="../../js/main.js" defer></script>
</head>
<body>
    {page_header("../../")}

    <main class="record-page">
        <article class="record-article">
            <p class="record-kicker">Codecademy Record {number:02d}</p>
            <h1>{escape(record["title"])}</h1>
            {source_html}
            {render_toc(sections)}
            <div class="record-content">
{render_sections(sections)}
            </div>
            <nav class="record-pagination">
                {previous_link}
                <a class="record-pagination-link index" href="../../learning/codecademy.html">All Codecademy records</a>
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


def render_platform_page(records: list[dict]) -> str:
    cards = []
    for index, record in enumerate(records, start=1):
        cards.append(
            f'''<a class="record-card" href="../records/codecademy/{record["slug"]}.html">
                <img src="../assets/records/thumbnails/codecademy/{index:02d}.svg" alt="{escape(record["title"])} cover image" loading="lazy">
                <div class="record-card-text">
                    <p class="record-card-number">Record {index:02d}</p>
                    <h2>{escape(record["title"])}</h2>
                </div>
            </a>'''
        )

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Aokun Lei's Codecademy learning records: web development and computer science course notes.">
    <title>Codecademy Records | Aokun Lei</title>
    <link rel="icon" href="../assets/images/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../css/style.css">
    <script src="../js/main.js" defer></script>
</head>
<body>
    {page_header("../")}

    <main class="records-index-page">
        <section class="records-intro">
            <p class="records-platform">Platform: Codecademy</p>
            <h1>Codecademy Records</h1>
            <p>{PLATFORM_INTRO}</p>
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
    RECORDS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    built: list[dict] = []

    for record in RECORDS:
        record_dir = ASSETS_DIR / record["slug"]
        if record["kind"] == "markdown":
            sections, source_url = build_markdown_sections(record)
        else:
            sections, source_url = build_docx_sections(record, record_dir)
        built.append({"record": record, "sections": sections, "source_url": source_url})

    for number, item in enumerate(built, start=1):
        record = item["record"]
        previous = built[number - 2]["record"] if number > 1 else None
        next_record = built[number]["record"] if number < len(built) else None
        page_path = RECORDS_OUTPUT_DIR / f"{record['slug']}.html"
        page_path.write_text(
            render_record_page(record, number, previous, next_record, item["sections"], item["source_url"]),
            encoding="utf-8",
        )
        print(f"Built {page_path.relative_to(ROOT).as_posix()} ({len(item['sections'])} sections)")

    PLATFORM_PAGE.parent.mkdir(parents=True, exist_ok=True)
    PLATFORM_PAGE.write_text(render_platform_page([item["record"] for item in built]), encoding="utf-8")
    print(f"Built {PLATFORM_PAGE.relative_to(ROOT).as_posix()} ({len(built)} records)")


if __name__ == "__main__":
    main()
