# Site maintenance context

This is the compact, durable project map for agents maintaining the personal website. It should explain where truth lives and highlight non-obvious lessons without trying to replace task-specific inspection.

## Canonical repository

Identify the working repository from Git metadata: its remote repository is `luck-lak/luck-lak.github.io`. Do not hard-code a machine-specific checkout path, and do not assume that a similarly named folder or staging copy is the canonical repository.

The site deliberately uses plain HTML, CSS, and a small amount of JavaScript. Jekyll supplies the blog and GitHub Pages build. Avoid introducing a framework unless a future requirement clearly justifies it.

## Project map

| Area | Primary source |
| --- | --- |
| Home page | `index.html` |
| Learning hub | `learning-records.html` |
| Platform lists | `learning/` |
| Course and paper pages | `records/` |
| Shared site styling | `css/style.css` |
| Shared browser behavior | `js/main.js` |
| Blog posts | `_posts/` |
| Blog layout and shared header | `_layouts/`, `_includes/` |
| Generated-page builders and checks | `tools/` |
| Deployment configuration | `_config.yml`, GitHub Pages workflow/state |

`README.md` and `README.en.md` are the human-facing maintenance guides. Keep them aligned when a durable public maintenance instruction changes.

## Generated learning records

`learning-records.html` is a manually maintained hub. Platform list and detail pages are generated:

- Codecademy: `tools/build_codecademy_records.py`; read its configuration for the current source directory, record registry, templates, and output paths. It defaults to a sibling `codecademy/` directory and accepts `CODECADEMY_NOTES_DIR` when the checkout lives elsewhere; keep the actual machine path out of versioned files.
- DeepLearning.AI: `tools/build_learning_records.py`; read the script and its registry for current inputs, covers, and outputs.

Do not directly edit generated detail or platform HTML when the generator owns the same markup; regeneration will overwrite it. Update the original note, generator data, or generator template, then rebuild. Platform totals in the hub may require a separate manual update; verify against current generated records rather than copying an old number.

Preserve original writing, bilingual tone, meaningful image order, and source links. Website introductions, navigation, and reusable presentation belong in templates or shared assets when possible.

## DOCX and code-note experience

- A Word document may store screenshots as floating anchored drawings. `python-docx` can report no inline shapes even when images exist; inspect paragraph XML for drawing relationships such as `a:blip` / `r:embed` and preserve paragraph order.
- Convert a code screenshot into semantic, selectable code only when its text and language can be reconstructed confidently. Keep the screenshot or mark uncertainty when visual information cannot be preserved faithfully.
- For code followed by explanatory annotations, use accessible code blocks plus nearby structured notes rather than forcing prose into the code block.
- Rebuilding a platform can update shared navigation, pagination, and many detail pages. Inspect the full diff rather than assuming only the new record changed.

## CSS and JavaScript conventions

Shared assets serve several page families. Scope new selectors and behavior to a component or page class so a record-page improvement does not leak into the home page or blog.

Substantial component sections need a short comment that states their purpose, with a visible boundary from neighboring components. Comments should explain intent or coupling, not narrate every declaration. Keep keyboard access, reduced-motion behavior, mobile layout, light/dark themes, and copy-button states in mind when the affected component uses them.

Long Codecademy records with reliable top-level sections can opt into the shared `record-page--chapter-cards` treatment through the record's `page_class` configuration. Use content length and real section structure as judgment signals; do not apply it automatically to every record whose generator kind happens to be `chapters`.

## Verification and publishing

Choose checks in proportion to the change. Useful checks include:

- rerun the relevant generator and confirm a second run produces no unexpected diff;
- inspect `git diff` and run `git diff --check`;
- validate local links and asset paths;
- render representative desktop and mobile widths, in light and dark themes;
- test navigation, table-of-contents jumps, and code-copy interactions when affected.

Publishing normally means committing and pushing the canonical repository's intended branch, then checking the GitHub Pages build and representative live URLs. Only publish when the user's request includes that scope. Determine the current branch, remote state, workflow result, and live content at execution time.

## Durable preferences

- Keep the implementation understandable and maintainable by the site owner.
- Preserve the author's personal voice and distinguish course material from personal reflection.
- Prefer semantic HTML and selectable code over text embedded in images when conversion is reliable.
- Keep CSS/JavaScript comments clear and component boundaries easy to scan.
- Treat this document as an information map, not a mandatory step-by-step workflow.

## Shared memory model

- `site-context.md` contains compact knowledge that is still true and useful across tasks.
- `maintenance-log.md` is the hot log for recent work and unresolved follow-ups; it is the only task history read by default.
- `history/YYYY.md` files are cold, append-only archives. Search them by component, filename, or task keyword only when earlier reasoning could affect the current task; do not load every archive for general orientation.

Rotate completed entries into their matching yearly archive when the hot log stops being quick to scan, spans several old maintenance phases, or contains work whose durable lessons are already represented here. This is a judgment call rather than a fixed entry or byte limit. Keep unresolved follow-ups hot regardless of age, preserve archived entries intact, and add dated corrections instead of rewriting history.

## Keeping this document useful

Add only facts likely to remain useful across multiple tasks: architecture, ownership boundaries, durable preferences, and expensive-to-rediscover pitfalls. Do not store record counts, latest commit hashes, current branches, absolute machine paths, or transient work-in-progress here. Those belong in Git/current files or the historical maintenance log.
