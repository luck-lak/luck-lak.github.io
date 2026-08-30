# AOKUN's Portfolio Website

A simple personal portfolio site built with plain HTML, CSS, and JavaScript.

## Project Structure

| Path | Purpose |
|---|---|
| `index.html` | Home page |
| `learning-records.html` | Learning records hub; intro statement, motivation and future direction, platform cards |
| `learning/` | One list page per platform |
| `records/` | One detail page per course or paper |
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
