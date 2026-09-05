# Agent maintenance log

This append-only journal lets different agents understand what prior maintenance tasks actually changed. It complements `site-context.md`; it is not a substitute for checking current repository state.

## Entry format

Append new entries at the bottom, newest last. Keep each entry concise and use only the fields that add value:

```markdown
### YYYY-MM-DD — Short task name

- Request: What the user wanted.
- Outcome: What is now true.
- Areas: Main files or components affected.
- Decisions: Non-obvious choices and why.
- Verification: Checks performed and their result.
- Publication: Local, committed, pushed, deployed, or deliberately not published.
- Follow-up: Remaining risk or useful next step; omit when none.
```

Do not include secrets, full command histories, large diffs, or cheap-to-derive snapshots. Keep history intact; add a dated correction if an older entry becomes misleading.

## History

### 2026-09-05 — Publish Bash and SQL learning records

- Request: Convert two new Codecademy DOCX notes into site records, improve code presentation, and add a simple SQL page table of contents.
- Outcome: Added the Bash and SQL records. A Bash code screenshot became selectable syntax-highlighted code with its annotations reorganized, and the SQL record gained a nine-item jump menu.
- Areas: Codecademy generator, platform navigation, record assets and pages, shared code/TOC styling and behavior.
- Decisions: Preserved the author's text and image order while moving reliably reconstructed code into semantic HTML.
- Verification: Rebuilt records, checked diffs and links, tested responsive/light-dark presentation and copy behavior, and confirmed the GitHub Pages deployment and live pages.
- Publication: Pushed to `main` in commit `1601f16`.

### 2026-09-05 — Clarify code component boundaries

- Request: Make the new CSS and JavaScript comments clear and visibly separated from other component code.
- Outcome: Refined the shared code-viewer and table-of-contents section comments and boundaries without changing behavior.
- Areas: `css/style.css`, `js/main.js`.
- Verification: Checked the diff and syntax-sensitive behavior; no functional regression was introduced.
- Publication: Pushed to `main` in commit `28de03d`.

### 2026-09-05 — Add shared maintenance memory

- Request: Create a reusable personal-site skill and an evolving agent-facing task record so future models do not rediscover the project from scratch.
- Outcome: Added a globally discoverable routing skill, a portable repository entry point, a stable project map, and this append-only task journal.
- Areas: `$luck-lak-site-maintenance`, `AGENTS.md`, `tools/agent/`, `_config.yml`.
- Decisions: Kept volatile state out of the skill; embedded promotion and pruning rules in the primary skill instead of creating a second meta-skill. Repository context remains usable by agents without skill support.
- Verification: Validated the skill structure, checked all documented repository paths, and performed a cold-start routing audit from the new entry files.
- Publication: Included in the site repository and pushed to `main` as part of this task; the agent-only files are excluded from the published site.
