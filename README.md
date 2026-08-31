# AOKUN's Portfolio Website

A simple personal portfolio site built with plain HTML, CSS, and JavaScript.

## Project Structure

| Path | Purpose |
|---|---|
| `index.html` | Home page |
| `learning-records.html` | Learning records hub; intro statement, motivation and future direction, platform cards |
| `learning/` | One list page per platform |
| `records/` | One detail page per course or paper |
| `_posts/`, `_layouts/`, `_includes/`, `blog/` | Jekyll source for the Blog section |
| `css/style.css` | Site-wide and learning-record styles |
| `js/main.js` | Small interactive behavior |
| `tools/` | Note-to-page build scripts and small inspection helpers |
| `assets/records/` | Record screenshots and navigation covers |
| `学习探索记录.docx` | Complete DeepLearning.AI source notebook |

## Adding New Content

For small updates, such as adding a new section or changing text:

1. Edit `index.html`.
2. Add corresponding styles in `css/style.css` if needed.
3. Add JavaScript in `js/main.js` only when interaction is required.

When adding a new section, keep the structure consistent:

```html
<section class="section-name">
    <h2>Section Title</h2>
    <p>Content...</p>
</section>
```

## Updating Projects

Projects are kept in the `#projects` section of `index.html`. To add one, copy a
`<article class="project-card">` block, then update the project name, GitHub link,
and one-sentence description. The card layout is already defined in
`css/style.css`, so no CSS changes are needed for a normal new project.

```html
<article class="project-card">
    <h3><a href="https://github.com/your-name/your-project">Project Name</a></h3>
    <p>A short description of what the project explores or does.</p>
</article>
```

## Learning Records

The records are organized by platform:

- `learning/deeplearning-ai.html` → `records/01…15-*.html`
- `learning/codecademy.html` → `records/codecademy/*.html`

Each detail page is generated from source notes. Do not edit generated HTML
for normal content updates; edit the source note or build script and rebuild.

| Platform | Build script | Source | Covers |
|---|---|---|---|
| DeepLearning.AI | `tools/build_learning_records.py` | `学习探索记录.docx` | `assets/records/thumbnails/NN.jpg/svg` |
| Codecademy | `tools/build_codecademy_records.py` | sibling `codecademy/` folder outside this repo | `assets/records/thumbnails/codecademy/NN.svg` |

## Tools In Plain Words

The build scripts are not part of the website itself. They convert source notes
into the HTML pages under `records/`. You do not need to run them by hand; the
assistant can update the matching script config, rebuild the pages, and check
links when you say that a new record is ready.

- Keep `build_learning_records.py` and `build_codecademy_records.py` while the
  site uses generated record pages.
- `inspect_docx.py` and `list_record_links.py` are one-off helpers for checking
  DOCX content and links. They can be deleted when no longer needed, but it is
  harmless to keep them.
- Do not delete a build script unless you are intentionally moving that platform
  back to hand-edited HTML.

## Adding a Codecademy Record

1. Put the new DOCX or Markdown file in the source `codecademy/` folder.
2. Add one entry to `RECORDS` in `tools/build_codecademy_records.py`, giving it
   a stable `title`, `slug`, and `kind`.
3. Draw a matching SVG cover at
   `assets/records/thumbnails/codecademy/NN.svg`.
4. Run:

   ```powershell
   & '<python>python.exe' -X utf8 tools/build_codecademy_records.py
   ```

5. Check the new detail page, previous/next links, platform page, and hub count.
6. Keep the original wording, screenshot order, and hyperlinks. Codecademy
   pages should not display DOCX links.

## Adding a New Platform

Use the same pattern as the two existing platforms:

1. Create `learning/<platform>.html` and `records/<platform>/`.
2. Create `tools/build_<platform>_records.py`.
3. Keep source files outside the site unless the user explicitly asks to
   archive them in the repository.
4. Put covers in `assets/records/thumbnails/<platform>/`.
5. Add one platform card to `learning-records.html`.
6. Update this README.

## Adjusting Layout or Styles

1. Make the change in `css/style.css`.
2. If a structural change affects generated HTML, update the matching build
   script and rebuild.
3. Verify desktop, mobile, and dark mode.
4. Keep generated pages consistent with the platform pages and hub.

## Local Preview

From the repository root:

```powershell
& '<python>python.exe' -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/`.

## Agent Notes

When updating learning records:

- Use the matching build script instead of hand-copying a whole page.
- Preserve the user's wording, screenshot order, and links.
- Keep the `learning-records.html` reading statement and platform cards intact.
- Keep the DOCX archive unchanged unless the user explicitly asks to update it.
- Update this README and the relevant build-script config when structure or
  conventions change.

## Blog (Jekyll)

The Blog section is built with Jekyll and hosted on GitHub Pages. It is fully
separate from Learning Records: Blog is for standalone writing (project
retrospectives, notes, ideas), while Learning Records remains the
platform-based course map. Pages without Jekyll front matter (all pre-existing
pages) pass through the build unchanged, so the rest of the site is not touched.

### Blog file structure

| Path | Purpose |
|---|---|
| `_config.yml` | Jekyll settings: permalink style (`/blog/:title/`) and build exclusions (`tools/`, README, DOCX archive) |
| `_posts/` | All blog posts as Markdown files |
| `_layouts/default.html` | Shared page shell for blog pages (header, nav, theme button, footer) |
| `_layouts/post.html` | Layout for a single post (date, title, content, back link) |
| `_includes/site-head.html` | Shared `<head>`: metadata, title, favicon, CSS, JavaScript, fonts |
| `_includes/site-header.html` | Shared fixed navigation and theme button |
| `_includes/site-footer.html` | Shared footer |
| `blog/index.html` | Blog list page; carries the full site shell directly and renders posts newest first with Liquid |
| `assets/images/blog/` | Post images, one subfolder per post |
| `css/style.css` | Blog styles live in the `/* ===== Blog (Jekyll) ===== */` section at the end of the file |
| `index.html`, `learning-records.html`, `learning/*.html` | Navigation entry points linking to `/blog/` |

### Build path

1. You push Markdown and layout files to `main`.
2. GitHub Pages runs Jekyll on their server; no local build is required.
3. `_posts/*.md` become `/blog/<slug>/` pages and `blog/index.html` becomes `/blog/`.
4. Build status is visible in the repository's Actions tab.

### Adding a new post

1. Create `_posts/YYYY-MM-DD-post-slug.md`. The filename date must be the
   publish date (future dates stay hidden until that date), and the slug
   becomes the URL: `/blog/post-slug/`.
2. Start the file with this front matter, then write Markdown below it:

```markdown
---
layout: post
title: "文章标题"
lang: zh
date: 2026-08-31 12:00:00 +0800
description: "列表页显示的一句话简介"
---
```

3. Put images in `assets/images/blog/<post-slug>/` and reference them with
   `/assets/images/blog/<post-slug>/image.png` (absolute path from site root).
4. Commit and push to `main`. The live site updates in a minute or two.

You can also add or edit posts directly on github.com: open the `_posts/`
folder, use "Add file" → "Create new file" with the same naming rules, then
commit to `main`.

### Changing blog styles

- List page styles: the `.blog-*` classes in the Blog section of `css/style.css`.
- Post page styles: the `.post-*` classes in the same section.
- Page structure (head, nav, footer): `_layouts/default.html`.
- Shared head, nav, and footer markup: `_includes/site-head.html`,
  `_includes/site-header.html`, and `_includes/site-footer.html`. The Blog list
  page includes them directly because it intentionally uses `layout: null` in
  this hybrid plain-HTML/Jekyll site.
- Post structure (date, title, content wrapper, back link): `_layouts/post.html`.
- Dark mode rules for both pages sit in the same CSS section; look for
  `body.dark-mode .blog-*` and `body.dark-mode .post-*`.

### Blog notes

- `description` is shown on the list page; without it, only the title and date show.
- `lang` (`zh` or `en`) sets the post page's `<html lang>` value.
- A midday time with `+0800` keeps the displayed date stable when GitHub builds in UTC.
- Learning Records detail pages keep their minimal nav (Home + Learning Records)
  by design; Blog is reachable from the hub pages.
