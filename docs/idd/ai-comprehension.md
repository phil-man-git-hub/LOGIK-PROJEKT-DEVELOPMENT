# AI Comprehension & Methodology

This document captures the methodology, assumptions, findings, and recommended next steps used by the automated reviewer (AI agent) while reading and summarizing the IDD documentation in this repository. It's intended to help maintainers, reviewers, and future automated agents reproduce the comprehension process and validate outputs.

## Purpose

- Record how the AI reads and synthesizes repository documentation.
- Preserve the methodology so human reviewers can verify and replicate steps.
- List key insights gathered while reviewing `docs/idd/` materials.
- Provide a clear set of next steps and tests to validate the IDD integration.

## Scope

Covers the reading and analysis approach used for the IDD documentation under `docs/idd/`. It documents how linked files were discovered, how content was prioritized, quality checks performed, and common assumptions taken during automated analysis.

---

## Methodology

1. Discover the documentation hub
   - Identify the primary hub document `docs/idd/README.md` as the authoritative index of linked materials.
   - Parse the README for explicit relative links to other files in `docs/idd/`.

2. Prioritize reading
   - Read the Quick Start (`quick_start.md`) first to understand user-facing steps.
   - Read architecture and system design docs to capture the overall system model and component interactions.
   - Read workflow and sync guides next to get actionable automation details (workflows, markers, configuration files).
   - Read templates and PR/Issue guides to capture conventions enforced by automation.
   - Read additional guides (troubleshooting, best-practices, metrics) for operational considerations.

3. Read documents in full where available
   - For each linked file, read the full markdown content and extract actionable items, commands, and file paths mentioned.
   - When file reads fail (missing files or path errors), record the missing paths for human review.

4. Extract artifacts and commands
   - Extract shell commands, script names, workflow filenames, and configuration keys to build a test/validation plan.
   - Note Python scripts and required environment variables for local testing (e.g. `GITHUB_TOKEN`, `GITHUB_REPOSITORY`).

5. Cross-reference
   - Cross-check labels, workflow names, and script paths across files to find mismatches or typos.
   - Verify that `idd-config.yml`, `.github/labels.yml`, and workflow files referenced actually exist (or mark them missing).

6. Produce summaries and suggested actions
   - Produce a concise summary of each major doc.
   - Produce a prioritized action list: missing files, scripts to test, workflows to enable, labels to create.

---

## Assumptions

- The `docs/idd/README.md` is the authoritative index of IDD materials for this repo.
- Automation scripts are located in `bin/` or `.github/scripts/` as indicated in the docs.
- GitHub Actions are enabled and `GITHUB_TOKEN` is available to workflows.
- Some files referenced in docs may be intentionally omitted in this repository; missing reads are recorded for manual verification.

---

## Key Insights (observed so far)

- The IDD system is heavily automation-driven: GitHub Actions + Python scripts form the core of synchronization, labeling, and AI context capture.
- Labels and labeler rules are central; they control grouping in `TO-DO.md` and automation behavior.
- The AI context system (`.ai-context/`) captures sessions, enables search, and allows context retrieval for assistants.
- The `TO-DO.md` auto-sync markers are important: manual edits inside auto-sync blocks are overwritten by automation.
- PR template enforces `Closes #N` style linking; automation relies on this for correct issue→PR linking.

---

## Recent updates (2025-11-12)

- Added `docs/idd/guides/guide-best-practices.md` to fill a missing link discovered in `docs/idd/README.md`.
- Confirmed README references are resolvable; the best-practices guide provides concrete contributor conventions that the AI used to refine suggestions.
- Clarified label governance guidance and tied it into the validation steps below.

---

## Validation & Tests (manual steps)

These are the minimal safe validations a maintainer can run locally to confirm the IDD integration is functioning as expected.

1. Environment preparation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Validate sync script (dry-run)

```bash
export GITHUB_TOKEN=$(gh auth token)
export GITHUB_REPOSITORY="phil-man-git-hub/LOGIK-PROJEKT-DEV"
python3 .github/scripts/sync_issues_to_todo.py --dry-run
# Inspect the output (it should show changes that would be made without committing)
```

3. Validate label sync (dry-run)

```bash
python3 .github/scripts/sync_labels.py --dry-run
# Or pass a test labels file to confirm mapping without applying
```

4. Trigger workflows manually via `gh` if needed

```bash
gh workflow run issue-to-todo-sync.yml --repo phil-man-git-hub/LOGIK-PROJEKT-DEV
gh workflow run auto-label.yml --repo phil-man-git-hub/LOGIK-PROJEKT-DEV
```

5. Inspect `.ai-context/` after a few changes to ensure session files are created.

---

## Common Pitfalls & Notes

- Case-sensitivity: macOS can mask case errors in filenames; ensure repository matches planned filenames exactly (e.g. `VERSION` vs `version`).
- Token scopes: local tests that hit the GitHub API should use a token with `repo` and `workflow` scopes if workflows or commit pushes are required.
- Branch protection: bot commits by workflows may be blocked by required status checks; test in a permissive branch or adjust protections temporarily.
- Auto-sync markers: Never edit the contents between `<!-- BEGIN AUTO-SYNC -->` and `<!-- END AUTO-SYNC -->` unless you intend to change automation.
- Label governance: changes to `.github/labels.yml` should follow the repository's ADR process and be verified with a dry-run of `sync_labels.py` before applying to GitHub.

---

## Links to related/new content

- Best practices guide: `docs/idd/guides/guide-best-practices.md` — contributor conventions (issues, PRs, labels, TO-DO sync, AI context).

---

## Recommended Next Actions


---

## Crucial IDD Workflow Information

## See also: [GitHub Issue AI Workflow Steps](github-issue-ai-workflow-steps.md)

### 🚀 AI-Augmented IDD Workflow (The "Turbocharged" Method)
The IDD process is now driven by the **Antigravity Agent** using the `.gemini/antigravity` "Second Brain". This allows for automated context management and zero-friction development.

#### Core Commands
*   **`/ag-load-issue <ID>`**: Ingests project context for an issue into the Agent's brain.
*   **`/ag-start-work <ID>`**: Automates the "Start" phase (Branch + Context + Plan).
*   **`/ag-sync-status`**: Automates status reporting to GitHub.
*   **`/ag-capture-all`**: Syncs the Agent's reasoning (Insights) with the Project's history (Git Logs).

### Generic To-Do Phases Template
 Automation scripts read this template and inject the phases/tasks into each new issue’s to-do file (e.g., `docs/idd/issues/issue-XX/step-51-to-do/to-do-issue-XX.md`).
- This ensures every issue starts with a consistent, actionable workflow and enables easy updates to the process by editing the template.

#### Example Usage in Automation
1. When a new issue is scaffolded, the script loads `github-issue-to-do-template.json`.
2. The script generates a markdown checklist for the issue’s to-do file, replacing placeholders (like `<issue-number>`) as needed.
3. Contributors and AI agents follow these phases for every issue, ensuring process consistency and traceability.

#### Template Structure
See [`github-issue-to-do-template.json`](github-issue-to-do-template.json) for the current phases and tasks.

#### Issue Directory Tree Template
For Phase 5 and directory scaffolding, see [`github-issue-tree-template.json`](github-issue-tree-template.json) for the standard issue directory and file structure.

### Issue Draft Storage
- Drafts for new GitHub Issues are stored in `docs/idd/issues/drafts/` (e.g., `ISSUE-001-add-idd-workflow.md`).
- This enables collaborative editing and review before publishing the issue on GitHub.

### Procedures After GitHub Issue Creation
- **Legacy Method**: Manually create branches and scaffold directories.
- **AI-Augmented Method**:
    1.  Run `/ag-start-work <issue-id>`.
    2.  The agent creates the branch `feature/issue-<id>-<desc>`.
    3.  The agent loads context and drafts `implementation_plan.md`.
    4.  Work begins immediately.

### Creation of Subdirectories and Documents
### Documentation of Memories and Decisions
- **Active Workspace**: The `.gemini/antigravity/` directory is the active workspace for "thinking" (Sessions, Research, Insights).
- **Bridge to Project**: The `/ag-capture-all` command bridges this private context to the public project record.
- **Legacy `step-61-memory/`**: This directory is still used for formal, finalized decision records, but the *process* of reaching those decisions happens in `.gemini`.

---

---

## Contact & Attribution

- Compiled by the automated agent during documentation review (Nov 2025). For questions, open an issue with label `idd` in this repository.

---

## Changelog for this document

- 2025-11-12 — Initial creation
- 2025-11-12 — Updated to reference and incorporate `guide-best-practices.md` and to add validation/next-step items
