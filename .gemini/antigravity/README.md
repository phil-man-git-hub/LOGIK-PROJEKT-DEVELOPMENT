# Antigravity Knowledge Base

This directory serves as a persistent "Second Brain" for the Antigravity AI assistant and the user. It stores project context, research, insights, and tasks that need to survive across individual chat sessions.

## Directory Structure

*   **`sessions/`**: Summaries of individual work sessions. What was done, what was decided, and what was left unfinished.
*   **`memory/`**: Long-term context, architectural decisions, and core project knowledge.
*   **`to-dos/`**: Active and backlog task lists.
*   **`research/`**: Raw research notes, data dumps, and investigation logs.
*   **`insights/`**: Synthesized knowledge, "aha!" moments, and summaries of complex topics.

## Naming Convention

All files in subdirectories (except this README) MUST follow this strict naming convention to ensure chronological sorting and easy scanning:

`YYYY-MM-DD-HH-MM-SS-<CATEGORY>-<BRIEF_DESCRIPTION>.md`

**Examples:**
*   `2025-11-22-09-15-00-session-initial-setup.md`
*   `2025-11-22-10-30-00-insight-authentication-flow.md`
*   `2025-11-22-14-00-00-research-pyside6-threading.md`

## Workflow Protocol

### 1. Start of Session
*   **Scan Context**: Read the latest files in `sessions/` and `to-dos/` to understand the current state of the project.
*   **Check Memory**: specific topics, check `memory/` or `insights/` for existing knowledge to avoid re-researching.

### 2. During Session
*   **Log Research**: If investigating a new topic, create a file in `research/`.
*   **Capture Insights**: When a conclusion is reached or a system is understood, summarize it in `insights/`.
*   **Update Todos**: If new tasks are discovered, add them to a file in `to-dos/`.

### 3. End of Session
*   **Session Summary**: Create a file in `sessions/` summarizing what was accomplished.
*   **Update State**: Mark completed items in `to-dos/`.
*   **Refine Memory**: If core project facts have changed, update or create files in `memory/`.

## Workflow Commands
*   `/ag-new`: Start a new session.
*   `/ag-save`: Save an insight, session summary, or research note.
*   `/ag-review`: Review long-term memory and insights.
*   `/ag-commit`: Generate a commit message and log it to the session.
*   `/ag-archive`: Archive old sessions and compress context.
*   `/ag-pr`: Prepare a Pull Request description.

## IDD Bridge Commands (Project Integration)
*   `/ag-load-issue`: Load context for a specific GitHub issue.
*   `/ag-start-work`: Start working on a new issue (branch + context + plan).
*   `/ag-sync-status`: Generate a status update for the GitHub issue.
*   `/ag-capture-all`: Capture session to both Antigravity and Project memory.
*   `/ag-scaffold-issue`: Scaffold standard directory structure for a new issue.
