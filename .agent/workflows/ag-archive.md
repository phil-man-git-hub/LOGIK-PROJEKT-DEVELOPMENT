---
description: Archive old sessions and compress insights to maintain a lean context.
---
1.  **Identify Old Sessions**:
    -   List files in \`.gemini/antigravity/sessions/\`.
    -   Identify sessions older than 7 days (or whatever threshold seems appropriate).

2.  **Compress Context**:
    -   Read the old session files.
    -   Extract any key decisions, architectural changes, or unsolved problems that are NOT yet in \`memory/\` or \`insights/\`.
    -   Update or create files in \`memory/\` or \`insights/\` with this consolidated information.

3.  **Archive**:
    -   Create directory \`.gemini/antigravity/sessions/archive/\` if it doesn't exist.
    -   Move the processed session files into the archive directory.

4.  **Report**:
    -   Tell the user: "I have archived [N] sessions and updated our long-term memory with [X] new insights."
