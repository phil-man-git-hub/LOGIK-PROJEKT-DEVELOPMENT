---
description: Prepare a Pull Request description based on the session context and recent commits.
---
1.  **Gather Context**:
    -   Read the current session log.
    -   Run \`git log origin/main..HEAD\` (or appropriate branch comparison) to see commits in this branch.

2.  **Draft PR Description**:
    -   Create a PR description following the project's template (if any).
    -   **Title**: Concise summary of the feature/fix.
    -   **Description**: Detailed explanation of *why* and *how*, referencing the insights from the session log.
    -   **Testing**: List verification steps performed (from the session log).

3.  **Present to User**:
    -   Output the draft markdown for the user to copy-paste into GitHub/GitLab.
