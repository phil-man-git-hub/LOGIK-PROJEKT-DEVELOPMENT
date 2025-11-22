# Insight: The IDD Bridge Strategy

## The Challenge
We have two "Brains":
1.  **Project Brain** (`.ai-context/`): The repository's shared memory, managed by `bin/` scripts.
2.  **Antigravity Brain** (`.gemini/antigravity/`): The agent's private "Second Brain" for reasoning and session context.

## The Solution: Bridge Workflows
We implemented a set of workflows to bridge these two systems, ensuring they stay in sync without manual effort.

### 1. Ingest (Project -> Agent)
*   **Workflow**: `/ag-load-issue`
*   **Mechanism**: Uses `bin/retrieve-context.py` to dump project knowledge into a markdown file, which the agent then reads to "load" the context.

### 2. Sync (Agent -> Project)
*   **Workflow**: `/ag-capture-all`
*   **Mechanism**:
    1.  Agent summarizes its own reasoning into `insights/`.
    2.  Agent runs `bin/capture-session.py` to log git activity.
    3.  (Future) Agent appends its summary to the project log.

### 3. Update (Agent -> GitHub)
*   **Workflow**: `/ag-sync-status`
*   **Mechanism**: Agent reads its own `task.md` and formats it into a GitHub comment, keeping the issue tracker alive.

## Benefit
This strategy allows the agent to be "stateful" and "aware" of the project's deep history while maintaining its own private workspace for reasoning and planning.
