---
description: Scaffold the standard directory structure and files for a new GitHub issue.
---
1.  **Get Issue Details**:
    -   Ask user for the **Issue ID** (e.g., 22).
    -   Ask user for the **Issue Title** (e.g., "Automate desktop app creation").

2.  **Create Directory**:
    -   Create directory: \`docs/idd/issues/issue-<IssueID>-<SanitizedTitle>/\`.

3.  **Scaffold Structure**:
    -   Based on \`docs/idd/issues/github-issue-tree-template.json\`, create the following subdirectories:
        -   \`step-01-issue-type/\`
        -   \`step-11-research/\`
        -   \`step-21-insight/\`
        -   \`step-31-cognition/\`
        -   \`step-41-how-to/\`
        -   \`step-51-to-do/\`
        -   \`step-61-memory/\`

4.  **Create Files**:
    -   Create empty markdown files in each subdirectory following the pattern: \`issue-<IssueID>-<step-name>.md\`.
    -   Example: \`step-11-research/issue-<IssueID>-research.md\`.

5.  **Populate To-Do**:
    -   Read \`docs/idd/issues/github-issue-to-do-template.json\`.
    -   Create \`step-51-to-do/issue-<IssueID>-to-do.md\` and populate it with the phases from the JSON template, converted to a markdown checklist.

6.  **Report**:
    -   Tell the user: "Scaffolded issue #<IssueID> at docs/idd/issues/issue-<IssueID>-...".
