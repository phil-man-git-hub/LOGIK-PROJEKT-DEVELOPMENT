---
description: Generate a commit message from context, commit changes, and log the commit to the current session file.
---
1.  **Analyze Changes**:
    -   Run \`git status\` and \`git diff --staged\` (or \`git diff\` if nothing staged).
    -   Review the current session log in \`.gemini/antigravity/sessions/\` to understand the *intent* behind the changes.

2.  **Generate Message**:
    -   Draft a conventional commit message (e.g., \`feat: ...\`, \`fix: ...\`) based on the changes and the session context.
    -   **Ask User**: "I propose the following commit message. Shall I proceed? [Message]"

3.  **Commit**:
    -   If approved, run \`git commit -m "..."\`.

4.  **Log to Session**:
    -   Append a note to the current session file:
        \`\`\`markdown
        - **Commit**: [Hash] - [Message]
        \`\`\`
