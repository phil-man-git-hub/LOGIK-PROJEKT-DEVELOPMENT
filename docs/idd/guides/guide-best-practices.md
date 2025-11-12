# IDD Best Practices

This guide collects recommended practices for working with the Issue-Driven Development (IDD) system in this repository. It complements the Quick Start, Workflows, Sync, and PR/Issue templates by turning design rules into actionable conventions teams should follow.

## Purpose

- Keep the repository consistent and automations reliable.
- Maximize signal in issues and PRs so automation can operate accurately.
- Preserve developer privacy and context while enabling AI-assisted workflows.

## Issue Best Practices

- Use the provided issue templates in `.github/ISSUE_TEMPLATE/`.
  - Choose the template that best fits (bug, feature, task, documentation, monitoring, research).
- Make titles short, descriptive, and prefixed where appropriate, e.g. `bug:`, `feat:`.
- Provide context and acceptance criteria in the body. Include steps to reproduce for bugs and expected outcomes for features.
- Add relevant labels (type, area, priority) when creating issues; automation will augment them but correct initial labels help grouping.
- Reference related issues or PRs with `Related: #NN` and close targets with `Closes #NN` when the PR will resolve the issue.
- Avoid creating duplicate issues; search before opening a new one.

## Pull Request Best Practices

- Use the repository PR template (`.github/pull_request_template.md`) and fill in all sections.
- Title must follow Conventional Commits (e.g., `feat(monitoring): add SNMPv3 support`).
- In the PR body include `Closes #NN` for each issue it resolves — automation relies on this to link commits/PRs to issues and to update the TO-DO sync.
- Keep PRs focused and reasonably sized. If a change spans multiple features, split into smaller PRs.
- Add tests and update documentation as part of the same PR.
- Use draft PRs while work is ongoing and mark ready for review when the checklist is complete.

## Commit & Branching Guidelines

- Use conventional commits in commit messages (type(scope): description).
- Branch naming: `feature/issue-<N>-short-desc`, `fix/issue-<N>-short-desc`, `chore/<topic>`.
- Squash or rebase as appropriate before merging to keep history tidy, but preserve meaningful commit content for session capture.

## Labeling and Taxonomy

- Maintain the canonical label definitions in `.github/labels.yml`.
- Use the labeler rules (`.github/labeler.yml` or workflow) to apply area labels based on paths changed.
- Common label categories:
  - Type: `bug`, `enhancement`, `documentation`, `chore`
  - Area: `monitoring`, `network`, `security`, `idd`, `infrastructure`
  - Priority: `priority/high`, `priority/medium`, `priority/low`
  - Status: `status/in-progress`, `status/needs-review`, `status/blocked`
- When adding new labels, update `.github/labels.yml` and run label sync tooling (or use the GitHub UI) to create them across the repository.

## TO-DO.md & Syncing

- Do not edit between the auto-sync markers in `TO-DO.md`:

```markdown
<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->
...
<!-- END AUTO-SYNC -->
```

- Add manual content outside the auto-sync blocks. The sync script will preserve manual sections.
- If you need an exception or a new auto-sync section, propose the change in an issue and update the sync script accordingly.

## AI Context & Session Capture

- The `.ai-context/` directory stores captured sessions and context indexes. Follow these guidelines:
  - Set privacy mode in `idd-config.yml` if you need to limit captured content (`none`, `minimal`, `standard`, `full`). Default is `standard` in many setups.
  - Avoid committing secrets, credentials, or API keys — add patterns to `idd-config.yml` exclude lists and `.gitignore` as needed.
  - Use explicit session capture (`bin/capture-session.py`) for major events (design sessions, major merges) to create clearer indexing points.

## GitHub Actions & Workflow Hygiene

- Keep workflow permissions minimal yet sufficient:
  - `contents: write` for workflows that commit files (TO-DO.md, docs)
  - `issues: write` for workflows that label or comment
  - `pull-requests: write` for PR automation
- When adding or editing workflows, test in a non-protected branch or a fork to avoid accidental bot commits to protected branches.
- Use `workflow_dispatch` for manual runs during testing.

## Testing & Validation

- Add unit tests for automation scripts in `tests/idd/` (e.g., `test_sync_issues.py`, `test_label_sync.py`).
- Include at least two test types for each script:
  - Happy path (non-empty issues, expected labels)
  - Edge case (empty issue set, missing markers)
- Lint workflow YAML files (`yamllint`) and validate GitHub Actions syntax through `act` or a test run.

## Security & Secrets

- Never commit secrets into the repository. Use repository secrets or environment variables in workflows.
- When running scripts locally that call the GitHub API, use a personal access token with the minimum necessary scopes, and revoke/regenerate when no longer needed.
- Mask secrets in logs where possible and sanitize session capture output.

## Performance & Rate Limiting

- The sync scripts are designed to be efficient; still, when running locally or in CI be mindful of GitHub API rate limits (5,000 requests/hour authenticated).
- Use caching and conditional requests (ETags) in scripts for heavy operations.

## Handling Breakages & Rollbacks

- If an automation commit is unexpected, use GitHub to revert the commit or manually revert the branch.
- Disable the faulty workflow temporarily by renaming the YAML file or pushing a fix to a branch and testing before enabling on main.

## Governance & Change Control

- Document changes to workflows, labels, and sync logic via an ADR (architecture decision record) in `architecture/decision-records/`.
- Small, incremental changes are preferred; coordinate cross-team changes (labels, templates) via an issue and a short rollout plan.

## FAQs (short)

- Q: "What if the TO-DO sync overwrote my manual edits?"
  - A: If edits were inside the auto-sync block, revert the TO-DO.md file from git history and reapply manual content outside the auto-sync markers. Open an issue to propose changing the sync behavior.

- Q: "How do I opt-out of AI context capture for a session?"
  - A: Set `ai_context.privacy_mode: none` in a local `idd-config.yml` (local override) or use `--privacy none` when running `bin/capture-session.py`.

- Q: "Who can change labels and workflows?"
  - A: Repository admins. For governance, open an issue describing the proposed label or workflow change, tag `idd` and `admin`.

---

## Example checklist (for contributors)

- [ ] Issue created using an appropriate template
- [ ] Branch named using the convention
- [ ] PR title follows conventional commit format
- [ ] PR body contains `Closes #N` for associated issues
- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] No secrets committed

---

*Last Updated: 2025-11-12*
