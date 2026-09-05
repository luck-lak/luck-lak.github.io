# Current agent maintenance log

This is the hot journal for recent personal-site work and unresolved follow-ups. It complements `site-context.md`; it is not a substitute for checking current repository state. Older completed work lives in `history/YYYY.md` and is searched only when relevant.

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

Do not include secrets, full command histories, large diffs, or cheap-to-derive snapshots. Keep unresolved follow-ups here even when they are old.

When this file is no longer a quick orientation aid, move completed entries intact to their matching yearly archive. Useful signals include several obsolete maintenance phases or lessons that have already been promoted to `site-context.md`; there is deliberately no fixed entry limit. Do not load archives by default or silently discard their contents.

## Current history

### 2026-09-05 — Add shared maintenance memory

- Request: Create a reusable personal-site skill and an evolving agent-facing task record so future models do not rediscover the project from scratch.
- Outcome: Added a globally discoverable routing skill, a portable repository entry point, a stable project map, and this append-only task journal.
- Areas: `$luck-lak-site-maintenance`, `AGENTS.md`, `tools/agent/`, `_config.yml`.
- Decisions: Kept volatile state out of the skill; embedded promotion and pruning rules in the primary skill instead of creating a second meta-skill. Repository context remains usable by agents without skill support.
- Verification: Validated the skill structure, checked all documented repository paths, and performed a cold-start routing audit from the new entry files.
- Publication: Included in the site repository and pushed to `main` as part of this task; the agent-only files are excluded from the published site.

### 2026-09-05 — Add hot and cold log layers

- Request: Prevent long-term maintenance history from consuming context or letting obsolete decisions distort current work.
- Outcome: Split agent history into a small current log and opt-in yearly archives, with relevance-based rotation and search rules.
- Areas: `$luck-lak-site-maintenance`, `AGENTS.md`, `tools/agent/site-context.md`, `tools/agent/maintenance-log.md`, `tools/agent/history/`.
- Decisions: Used qualitative rotation signals instead of a fixed entry count; unresolved follow-ups remain hot regardless of age, while archived entries remain intact and are not read by default.
- Verification: Validated the updated skill, confirmed archived entries were preserved, checked routing language across all agent entry files, and inspected the repository diff.
- Publication: Committed and pushed to `main` as part of this task; all agent-memory files remain excluded from the published site through the existing `tools` exclusion.
