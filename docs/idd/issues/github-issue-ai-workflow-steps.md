
# GitHub Issue AI Workflow Steps

## Introduction

This document describes the standardized, AI-driven workflow steps for managing GitHub Issues in LOGIK-PROJEKT-DEV. It is designed for maintainers, contributors, and AI agents to ensure every issue follows a consistent, actionable process from draft to completion.

---

## Table of Contents
1. [Introduction](#introduction)
2. [LLM-Assisted Issue Creation Note](#llm-assisted-issue-creation-note)
3. [Example: LLM-Assisted GitHub Issue Creation](#example-llm-assisted-github-issue-creation)
4. [Workflow Overview](#workflow-overview)
5. [Sustainability Interpretation](#sustainability-interpretation)
6. [Next Steps](#next-steps)

---

## LLM-Assisted Issue Creation Note

> **Note:** Users can prompt a large language model (LLM) to "Create GitHub Issue" and enter into a conversation about the nature of the Issue. This allows the LLM to rationalize user desires and generate GitHub Issues that are conventional, concise, and comprehensive, improving both clarity and workflow hygiene.

[Back to TOC](#table-of-contents)

---

## Example: LLM-Assisted GitHub Issue Creation

**User:** Create GitHub Issue for automating desktop app creation for Flame 2027.0.0.

**LLM:** Can you clarify the platforms and expected user experience? Should the automation support both macOS and Linux, and include desktop entry creation?

**User:** Yes, support both platforms. Automate .app and .desktop file creation, and ensure the Python interpreter is detected automatically.

**LLM:** Thank you! Here is a conventional, concise, and comprehensive GitHub Issue:

---
**Title:** [FEATURE] Automate desktop app creation for Flame 2027.0.0 (#42)

**Description:**
Automate the creation of desktop application launchers for LOGIK-PROJEKT on both macOS and Linux. The workflow should:
- Detect the Autodesk Python interpreter automatically
- Generate `.app` bundles for macOS and `.desktop` entries for Linux
- Copy icons and set up Info.plist and shell scripts
- Ensure cross-platform compatibility and robust error handling

**Checklist:**
- [ ] Supports macOS and Linux
- [ ] Detects Python interpreter
- [ ] Creates `.app` and `.desktop` files
- [ ] Copies icons and sets metadata
- [ ] Validates automation with tests

**Linked Issue:** Closes #42
---

This conversational approach allows the LLM to rationalize user desires and generate issues that are conventional, concise, and comprehensive.

[Back to TOC](#table-of-contents)

---

## Workflow Overview

1. **Draft Creation**
   - Store initial issue drafts in [`docs/idd/issues/drafts/`](../issues/drafts/) for collaborative editing.

2. **Issue Publication**
   - Publish the issue on GitHub using a template from [`.github/ISSUE_TEMPLATE/`](../../../.github/ISSUE_TEMPLATE/).
   - Assign labels and link related documentation.

3. **Branch & Directory Setup**
   - Create a related branch (e.g., `issue-XX-description`).
   - Scaffold the issue directory: [`docs/idd/issues/issue-XX/`](../issues/).
   - Link branch and PR to the GitHub Issue (e.g., “Closes #XX”).

4. **To-Do Phases Injection**
   - Automation reads [`github-issue-to-do-template.json`](github-issue-to-do-template.json) and injects generic phases/tasks into [`step-51-to-do/README.md`](step-51-to-do/README.md).
   - Phases include: Feature Definition, Research, Insight, Implementation, Review, Memory, Finalization.

5. **Subdirectory & Document Creation**
    - Automation reads [`github-issue-tree-template.json`](github-issue-tree-template.json) to scaffold the standard subdirectories and files for each workflow step.
    - Typical structure includes:
      - [`step-01-issue-type/`](step-01-issue-type/), [`step-11-research/`](step-11-research/), [`step-21-insight/`](step-21-insight/), [`step-31-cognition/`](step-31-cognition/), [`step-41-how-to/`](step-41-how-to/), [`step-51-to-do/`](step-51-to-do/), [`step-61-memory/`](step-61-memory/)
    - Each subdirectory is populated with a README or markdown file as defined in the template.

6. **Automated Population & Updates**
   - Scripts fill in initial context, metadata, and placeholders.
   - Automation updates to-do checklists, session logs, and decision records as work progresses.

7. **Memory & Decision Documentation**
   - Use [`step-61-memory/`](step-61-memory/) to record key decisions, rationale, and session history before final commit.

8. **Finalization & PR**
   - Prepare PR with correct issue linking.
   - Ensure all automation checks and documentation are complete.

[Back to TOC](#table-of-contents)

---

## Sustainability Interpretation

- **Consistency:** Every issue follows the same phases and directory structure, reducing confusion and onboarding time.
- **Automation:** Scripts and workflows handle repetitive setup, updates, and documentation, minimizing manual effort.
- **Traceability:** All work, decisions, and context are captured in dedicated files and directories, ensuring future maintainers and AI agents can understand the history.
- **Extensibility:** The template and workflow can be updated centrally (e.g., editing `github-issue-to-do-template.json`), propagating improvements to all future issues.
- **Transparency:** Human-readable documentation and machine-readable templates make the process clear for both contributors and automation.
- **Reviewability:** Each phase and step is documented, making it easy to audit progress, review work, and ensure nothing is missed.

[Back to TOC](#table-of-contents)

---

## Next Steps

- Integrate this workflow into onboarding and contribution guides.
- Periodically review and update the template and documentation for improvements.
- Monitor automation for reliability and adjust as needed.
