# Personal website agent entry point

This repository is maintained by different models and agents. For any substantive website task:

1. Read `tools/agent/site-context.md` for the stable project map and source-of-truth boundaries.
2. Read the latest relevant entries in `tools/agent/maintenance-log.md` for recent decisions and prior verification. The log is historical context, not proof of current state.
3. Inspect current Git state and only the files relevant to the request before editing.
4. Append a concise maintenance-log entry when the task is complete. Skip trivial conversation and repeated status checks.

If the personal skill `$luck-lak-site-maintenance` is available, use it. These repository files remain the portable fallback for agents that do not support Codex skills.

Prefer generators and original notes over direct edits to generated pages. Preserve unrelated user changes. Commit, push, deployment, and other external writes require the scope of the user's request to include them.

Update `site-context.md` only for durable architecture, conventions, or preferences. Put one-task outcomes in the append-only log, and derive volatile facts such as counts, active branches, latest commits, and local paths from the repository when needed.
