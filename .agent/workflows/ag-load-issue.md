---
description: Load context for a specific GitHub issue using the project's existing scripts.
---
1.  **Retrieve Context**:
    -   Run the project's context retrieval script:
        \`python bin/retrieve-context.py --issue <ISSUE_ID> -o .gemini/antigravity/memory/issue-<ISSUE_ID>-context.md\`

2.  **Ingest Context**:
    -   Read the newly created file: \`.gemini/antigravity/memory/issue-<ISSUE_ID>-context.md\`.

3.  **Start Session**:
    -   Run the \`/ag-new\` workflow (or manually create a session file) focused on this issue.
    -   **Session Goal**: "Address Issue #<ISSUE_ID>"
