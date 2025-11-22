---
description: Start working on a new issue: creates branch, loads context, and prepares plan.
---
1.  **Create Branch**:
    -   Ask user for a short description if not provided.
    -   Run \`git checkout -b feature/issue-<ISSUE_ID>-<DESCRIPTION>\`.

2.  **Load Context**:
    -   Execute the \`/ag-load-issue\` workflow for this issue ID.

3.  **Prepare Plan**:
    -   Create or update \`implementation_plan.md\`.
    -   **Header**: \`# Issue #<ISSUE_ID>: <DESCRIPTION>\`
    -   **Content**: Fill in the standard implementation plan template based on the loaded context.

4.  **Notify**:
    -   Tell the user: "Branch created, context loaded, and plan drafted. Ready to review the plan?"
