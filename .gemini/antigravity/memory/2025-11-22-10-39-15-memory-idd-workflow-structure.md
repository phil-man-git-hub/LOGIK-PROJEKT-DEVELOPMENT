# Memory: IDD Workflow Structure

## Core Components
1.  **Issue Directory**: `docs/idd/issues/issue-<ID>-<TITLE>/`
2.  **Standard Steps**:
    *   `step-01-issue-type`: Feature definition.
    *   `step-11-research`: Background info.
    *   `step-21-insight`: Analysis and planning.
    *   `step-31-cognition`: Deep thinking/reasoning.
    *   `step-41-how-to`: User guides.
    *   `step-51-to-do`: Task tracking (checklist).
    *   `step-61-memory`: Decision records.

## Templates
*   **Tree**: `docs/idd/issues/github-issue-tree-template.json` defines the folder structure.
*   **To-Do**: `docs/idd/issues/github-issue-to-do-template.json` defines the standard phases.

## Automation
*   The `/ag-scaffold-issue` workflow automates the creation of this structure.
