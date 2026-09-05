from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path
import os
import re

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.hyperlink import Hyperlink
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get("CODECADEMY_NOTES_DIR", ROOT.parent / "codecademy")).expanduser().resolve()
RECORDS_OUTPUT_DIR = ROOT / "records" / "codecademy"
ASSETS_DIR = ROOT / "assets" / "records" / "codecademy"
THUMBNAILS_DIR = ROOT / "assets" / "records" / "thumbnails" / "codecademy"
PLATFORM_PAGE = ROOT / "learning" / "codecademy.html"

PLATFORM_INTRO = (
    "Notes from Codecademy courses on web development, systems, and data foundations, "
    "with chapter summaries, code examples, screenshots, and personal reflections."
)

# 保留平台页原有的个人序言；重新生成页面时不会丢失。
PLATFORM_PREFACE = '''
        <section class="platform-preface">
            <h2>Codecademy Platform Preface</h2>
            <p>Learn HTML是我在codecademy平台接触的第一门课，应该是我想学习搭建网站的时候AI推荐的学习资源，这个平台和我原来习惯的视频学习方式很不同，刚开始也只是想着没事像闯关一样玩一下，然后逐渐发现乐趣。</p>
            <p>虽然现在我感觉我的网页开发水平也只是入门，但在当时当我发现我可以自己写HTML并在网页显示的时候，是很惊喜的。</p>
            <p>通过这门课，我解锁了codecademy这个平台，感觉这个平台对于快速学习一些技术是挺有帮助的。</p>
            <p>这个平台的记录一般是我复制每个章节最后的review整合到一起，原意是便于自己回忆，但是其实感觉我想回忆相关知识倒也不会看这些，因为codecademy对于大部分课程都有cheatsheet可以用来回顾。</p>
            <p>当前的记录方式其实不是很利于读者阅读，我把这些笔记留在这里主要是做个标记，读者也可以大致浏览知道每门课的内容，但是我不是很建议单纯使用这些笔记来学习，我认为这可能会毁了你的学习体验。后续挺多节课的记录方式都基本都是这样，但对于新笔记我会采取新的方式(按顺序应该在Learn the Command Line课程后面)，应该是在开头写自己的总结和收获，希望更利于读者阅读与学习。</p>
        </section>
'''

BASH_BUILD_SCRIPT = '''#!/bin/bash

echo "Welcome to the build script!"

firstline=$(head -n 1 changelog.md)

read -a splitfirstline <<< $firstline

version=${splitfirstline[1]}

echo "You are building version $version."

echo "Is this the correct version?"
echo "Enter 1 to continue, or 0 to exit."

read versioncontinue

if [ $versioncontinue -eq 1 ]
then
  echo "OK"

  for filename in source/*
  do
    echo "Found file: $filename"

    if [ $filename == "source/secretinfo.md" ]
    then
      echo "$filename is not being copied."
    else
      echo "$filename is being copied."
      cp "$filename" build/
    fi
  done

  cd build/

  echo "Build version $version contains:"
  ls

  cd ..
else
  echo "Please come back when you are ready"
fi'''

# One entry per course. "kind" chooses how the document is split:
#   chapters   - split on 第X章章节总结（Topic） markers
#   flat       - one flowing section, headings and tables stay inline
#   sectioned  - split on record-specific section markers
#   cheatsheet - split on exact "cheat_headings" lines, render code and tables
#   markdown   - split on "# " headings in a Markdown file
RECORDS = [
    {
        "file": "frontend/Learn HTML.docx",
        "title": "Learn HTML",
        "slug": "learn-html",
        "kind": "chapters",
        "page_class": "record-page--chapter-cards",
    },
    {
        "file": "frontend/Learn CSS.docx",
        "title": "Learn CSS",
        "slug": "learn-css",
        "kind": "chapters",
        "page_class": "record-page--chapter-cards",
    },
    {
        "file": "frontend/CSS intermidiate.docx",
        "title": "Intermediate CSS",
        "slug": "intermediate-css",
        "kind": "chapters",
        "page_class": "record-page--chapter-cards",
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
        "page_class": "record-page--chapter-cards",
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
    {
        "file": "Learn Bash Scripting.docx",
        "title": "Learn Bash Scripting",
        "slug": "learn-bash-scripting",
        "kind": "sectioned",
        "section_markers": {
            "课程总结": "Course Summary",
            "这个课程的第一节还挺有意思的，": "Notes and Takeaways",
            "然后一个最后项目写的构建脚本：": "Final Project Build Script",
            "附带解释：": "Annotated Build Script",
        },
        "code_images": {
            1: {"label": "Bash", "language": "bash", "code": BASH_BUILD_SCRIPT},
        },
        "code_ranges": [
            {
                "start": "#!/bin/bash",
                "to_end": True,
                "after_section": "Annotated Build Script",
                "label": "Bash · annotated",
                "language": "bash",
            },
        ],
    },
    {
        "file": "Analyse  Data with SQL.docx",
        "title": "Analyze Data with SQL",
        "slug": "analyze-data-with-sql",
        "kind": "chapters",
        "page_class": "record-page--chapter-cards",
        "demote_heading_1": True,
        "promote_headings": ["SQLite Summary", "SQL Window Functions Summary"],
        "section_markers": {"问题自查清单：": "问题自查清单"},
        "code_ranges": [
            {"start": "CREATE TABLE celebs (", "end": ");", "label": "SQL", "language": "sql"},
            {"start": "sqlite3 newdb.sqlite", "end": "sqlite3 newdb.sqlite", "label": "Shell", "language": "shell"},
            {"start": "sqlite>", "end": "sqlite>", "label": "SQLite prompt", "language": "output"},
            {"start": ".exit", "end": ".exit", "label": "SQLite", "language": "sql"},
            {"start": "function() OVER (", "end": ")", "label": "SQL", "language": "sql"},
            {"start": "AVG(salary) OVER (", "end": ")", "label": "SQL", "language": "sql"},
            {"start": "RANK() OVER (", "end": ")", "label": "SQL", "language": "sql"},
        ],
    },
]

CHAPTER_PATTERN = re.compile(r"^第([一二三四五六七八九十\d]+)章+章节总结(?:[（(](.+?)[)）])?[:：]?\s*$")
CHAPTER_NUMBERS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
SITE_LINK_PATTERN = re.compile(r"^(?:课程网址|网站)[:：]")
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


def highlight_variables(text: str) -> str:
    """Highlight shell variables inside a quoted string."""
    pattern = re.compile(r"(\$\{[^}]+\}|\$[A-Za-z_][A-Za-z0-9_]*)")
    parts = []
    position = 0
    for match in pattern.finditer(text):
        parts.append(escape(text[position:match.start()]))
        parts.append(f'<span class="syntax-variable">{escape(match.group(0))}</span>')
        position = match.end()
    parts.append(escape(text[position:]))
    return "".join(parts)


def highlight_bash_line(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#!"):
        prefix = escape(line[: len(line) - len(stripped)])
        return prefix + f'<span class="syntax-shebang">{escape(stripped)}</span>'
    if stripped.startswith("#"):
        prefix = escape(line[: len(line) - len(stripped)])
        return prefix + f'<span class="syntax-comment">{escape(stripped)}</span>'

    token_pattern = re.compile(
        r'("(?:\\.|[^"\\])*")'
        r'|(\$\{[^}]+\}|\$[A-Za-z_][A-Za-z0-9_]*|\$\()'
        r'|(<<<|==|-eq|-ne|-le|-lt|-ge|-gt)'
        r'|\b(if|then|else|fi|for|in|do|done)\b'
        r'|\b(echo|read|head|cp|cd|ls)\b'
        r'|\b(\d+)\b'
    )
    parts = []
    position = 0
    for match in token_pattern.finditer(line):
        parts.append(escape(line[position:match.start()]))
        token = match.group(0)
        if match.group(1):
            parts.append(f'<span class="syntax-string">{highlight_variables(token)}</span>')
        elif match.group(2):
            parts.append(f'<span class="syntax-variable">{escape(token)}</span>')
        elif match.group(3) or match.group(6):
            parts.append(f'<span class="syntax-number">{escape(token)}</span>')
        elif match.group(4):
            parts.append(f'<span class="syntax-keyword">{escape(token)}</span>')
        elif match.group(5):
            parts.append(f'<span class="syntax-command">{escape(token)}</span>')
        position = match.end()
    parts.append(escape(line[position:]))
    return "".join(parts)


def highlight_sql_line(line: str) -> str:
    token_pattern = re.compile(
        r"('(?:''|[^'])*')"
        r'|\b(CREATE|TABLE|SELECT|FROM|WHERE|INSERT|INTO|UPDATE|DELETE|ALTER|'
        r'PARTITION|BY|ORDER|OVER|AS|DESC|ASC|INTEGER|TEXT|NULL)\b'
        r'|\b(\d+(?:\.\d+)?)\b',
        re.IGNORECASE,
    )
    parts = []
    position = 0
    for match in token_pattern.finditer(line):
        parts.append(escape(line[position:match.start()]))
        token = escape(match.group(0))
        if match.group(1):
            parts.append(f'<span class="syntax-string">{token}</span>')
        elif match.group(2):
            parts.append(f'<span class="syntax-keyword">{token}</span>')
        else:
            parts.append(f'<span class="syntax-number">{token}</span>')
        position = match.end()
    parts.append(escape(line[position:]))
    return "".join(parts)


def highlight_code(code: str, language: str) -> str:
    if language == "bash":
        return "\n".join(highlight_bash_line(line) for line in code.splitlines())
    if language == "sql":
        return "\n".join(highlight_sql_line(line) for line in code.splitlines())
    return escape(code)


def code_block_html(code: str, label: str, language: str) -> str:
    highlighted = highlight_code(code, language)
    return (
        '<div class="record-code-block">'
        '<div class="record-code-header">'
        f'<span class="record-code-language"><span aria-hidden="true">&lt;/&gt;</span> {escape(label)}</span>'
        '<button class="code-copy-button" type="button">Copy</button>'
        '</div>'
        f'<pre><code class="language-{escape(language, quote=True)}">{highlighted}</code></pre>'
        '</div>'
    )


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


def save_images(paragraph: Paragraph, record: dict, record_dir: Path, counter: list[int], html: list[str]) -> None:
    for image_id in paragraph._p.xpath(".//a:blip/@r:embed"):
        counter[0] += 1
        replacement = record.get("code_images", {}).get(counter[0])
        if replacement:
            html.append(
                code_block_html(
                    replacement["code"],
                    replacement.get("label", "Code"),
                    replacement.get("language", "text"),
                )
            )
            continue
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
    code_capture: dict | None = None
    code_lines: list[str] = []
    code_starts: dict[str, list[dict]] = {}
    for item in record.get("code_ranges", []):
        code_starts.setdefault(item["start"], []).append(item)
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

    def flush_code() -> None:
        nonlocal code_capture, code_lines
        if code_capture is not None:
            compact_lines = []
            for line in code_lines:
                if not line and compact_lines and not compact_lines[-1]:
                    continue
                compact_lines.append(line)
            code = "\n".join(compact_lines).strip("\n")
            current_section()["html"].append(
                code_block_html(
                    code,
                    code_capture.get("label", "Code"),
                    code_capture.get("language", "text"),
                )
            )
        code_capture = None
        code_lines = []

    def add_text(block: Paragraph, text: str, style: str) -> None:
        nonlocal source_url, main_started
        normalized_text = re.sub(r"\s+", " ", text).casefold()
        if normalized_text == normalized_title:
            return  # the document repeats the course title; the page header has it

        if SITE_LINK_PATTERN.match(text) and not main_started:
            if source_url is None:
                source_url = extract_source_url(block)
            return  # the course link moves to the page header

        section_title = record.get("section_markers", {}).get(text)
        if section_title is not None:
            flush_cheat()
            flush_list()
            main_started = True
            used["section"] = start_section(sections, section_title)
            return

        if kind == "chapters":
            chapter = chapter_heading(text)
            if chapter is not None:
                flush_cheat()
                flush_list()
                main_started = True
                title = f"Chapter {chapter[0]}: {chapter[1]}" if chapter[1] else f"Chapter {chapter[0]}"
                used["section"] = start_section(sections, title)
                return

        if style == "Heading 1" and text in record.get("promote_headings", []):
            flush_cheat()
            flush_list()
            main_started = True
            used["section"] = start_section(sections, text)
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
        if style == "Heading 1" and not record.get("demote_heading_1"):
            section["html"].append(f"<h2>{inline_html(block)}</h2>")
        elif style in {"Heading 1", "Heading 2", "Heading 3"}:
            section["html"].append(f"<h3>{inline_html(block)}</h3>")
        elif is_label_line(text):
            section["html"].append(f"<h3>{inline_html(block)}</h3>")
        else:
            section["html"].append(f"<p>{inline_html(block)}</p>")

    for block in iter_blocks(document):
        if isinstance(block, Table):
            flush_code()
            flush_cheat()
            flush_list()
            current_section()["html"].append(table_html(block))
            continue

        text = paragraph_text(block)

        if code_capture is not None:
            code_lines.append(block.text.rstrip())
            if not code_capture.get("to_end") and text == code_capture.get("end"):
                flush_code()
            continue

        range_config = next(
            (
                item
                for item in code_starts.get(text, [])
                if not item.get("after_section")
                or (
                    used["section"] is not None
                    and used["section"]["title"] == item["after_section"]
                )
            ),
            None,
        )
        if range_config is not None:
            flush_cheat()
            flush_list()
            code_capture = range_config
            code_lines = [block.text.rstrip()]
            if not range_config.get("to_end") and text == range_config.get("end"):
                flush_code()
            continue

        if text and SITE_LINK_PATTERN.match(text) and not sections and source_url is None:
            source_url = extract_source_url(block)
            if kind == "chapters":
                continue  # the course link moves to the page header

        if block.style.name != "List Paragraph":
            flush_list()
        image_ids = block._p.xpath(".//a:blip/@r:embed")
        if image_ids:
            section = current_section()
            save_images(block, record, record_dir, image_counter, section["html"])
        if text:
            add_text(block, text, block.style.name)

    flush_code()
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
            <a href="{relative_root}index.html#current-focus">Current Focus</a>
            <a href="{relative_root}learning-records.html" class="active">{active}</a>
            <a href="{relative_root}blog/">Blog</a>
        </nav>
        <button class="theme-button" type="button">🌙</button>
    </header>'''


def render_record_page(record: dict, number: int, previous: dict | None, next_record: dict | None, sections: list[dict], source_url: str | None) -> str:
    pagination_links = []
    if previous:
        pagination_links.append(
            f'<a class="record-pagination-link previous" href="{previous["slug"]}.html">Previous</a>'
        )
    pagination_links.append(
        '<a class="record-pagination-link index" href="../../learning/codecademy.html">All Codecademy records</a>'
    )
    if next_record:
        pagination_links.append(
            f'<a class="record-pagination-link next" href="{next_record["slug"]}.html">Next</a>'
        )
    pagination_html = "\n".join(f"                {link}" for link in pagination_links)
    source_html = ""
    if source_url:
        url = escape(source_url, quote=True)
        source_html = f'<p class="record-source"><a href="{url}" target="_blank" rel="noopener noreferrer">Course page</a></p>'
    page_class = "record-page"
    if record.get("page_class"):
        page_class += f' {escape(record["page_class"], quote=True)}'

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

    <main class="{page_class}">
        <article class="record-article">
            <p class="record-kicker">Codecademy Record {number:02d}</p>
            <h1>{escape(record["title"])}</h1>
            {source_html}
            {render_toc(sections)}
            <div class="record-content">
{render_sections(sections)}
            </div>
            <nav class="record-pagination">
{pagination_html}
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
    <meta name="description" content="Aokun Lei's Codecademy learning records: web development, systems, and data course notes.">
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

{PLATFORM_PREFACE}

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
