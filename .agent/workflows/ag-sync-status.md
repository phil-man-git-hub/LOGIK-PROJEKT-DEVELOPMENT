---
description: Generate a status update for the GitHub issue based on current progress.
---
1.  **Analyze Progress**:
    -   Read \`task.md\` to see completed items.
    -   Read the current session log.

2.  **Draft Comment**:
    -   Create a markdown comment summarizing:
        -   **Completed**: List of finished tasks.
        -   **In Progress**: What is currently being worked on.
        -   **Blockers**: Any issues preventing progress.

3.  **Post (Optional)**:
    -   If \`gh\` CLI is available, ask user if they want to auto-post:
        \`gh issue comment <ISSUE_ID> --body-file <TEMP_FILE>\`
    -   Otherwise, print the comment for the user to copy.
