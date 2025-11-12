# IDD Best Practices

Guidelines and recommendations for effective Issue-Driven Development.

## Table of Contents

- [Issue Management](#issue-management)
- [Commit Practices](#commit-practices)
- [Pull Request Workflow](#pull-request-workflow)
- [Label Strategy](#label-strategy)
- [Documentation](#documentation)
- [Team Collaboration](#team-collaboration)
- [Code Review](#code-review)
- [Workflow Optimization](#workflow-optimization)

---

## Issue Management

### Creating Good Issues

✅ **DO:**
- Use issue templates
- Provide clear, descriptive titles
- Include all required information
- Add relevant labels
- Link to related issues
- Include acceptance criteria
- Estimate effort when possible

❌ **DON'T:**
- Create vague issues ("fix stuff")
- Skip the template
- Forget to add labels
- Create duplicate issues
- Mix multiple concerns in one issue

### Example: Good Feature Request

```markdown
Title: feat: Add user profile photo upload

## Description
Users should be able to upload a profile photo to personalize their account.

## Use Case
As a user, I want to upload a profile photo so that other users can recognize me.

## Acceptance Criteria
- [ ] User can select image file
- [ ] Image is validated (size, format)
- [ ] Image is displayed on profile
- [ ] Image can be updated/removed
- [ ] Works on mobile and desktop

## Technical Notes
- Max size: 5MB
- Formats: JPG, PNG, GIF
- Store in S3, CDN delivery
- Generate thumbnails (100x100, 400x400)

## Related
- Related to #42 (User profiles)
- Depends on #43 (S3 integration)

Labels: enhancement, user-facing, effort:medium
```

### Issue Lifecycle

```
Created → Labeled → Assigned → In Progress → PR Created → PR Reviewed → Merged → Closed
```

**Best Practice:**
- Update issue status with labels: `in-progress`, `blocked`, `needs-review`
- Comment on progress regularly
- Close issues promptly after merging PR

---

## Commit Practices

### Conventional Commits

Use conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes bug nor adds feature
- `test`: Adding missing tests
- `chore`: Maintain. Changes to build process or tools
- `ci`: CI/CD changes
- `perf`: Performance improvement

**Examples:**

✅ **GOOD:**
```bash
git commit -m "feat: add user authentication (#42)"
git commit -m "fix: resolve null pointer in login handler (#43)"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify database connection logic"
```

❌ **BAD:**
```bash
git commit -m "changes"
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdfasdf"
```

### Linking Commits to Issues

Always reference issues in commits:

```bash
# Direct reference
git commit -m "feat: implement user login #42"

# Closing keywords
git commit -m "fix: resolve bug, closes #43"
git commit -m "feat: add feature, fixes #44"
git commit -m "docs: update guide, resolves #45"

# Multiple issues
git commit -m "feat: implement auth (#42, #43)"
```

**Supported Keywords:**
- `closes #123`
- `fixes #123`
- `resolves #123`
- `#123` (reference only)

### Commit Size

**Ideal:**
- One logical change per commit
- Commit frequently (multiple times per day)
- Keep commits focused and atomic

**Example Good Commit History:**
```
feat: add user model
feat: add user controller
feat: add user views
test: add user tests
docs: document user API
```

**Example Bad Commit History:**
```
WIP
more changes
final changes
actually final changes
```

---

## Pull Request Workflow

### Creating Pull Requests

✅ **DO:**
- Use conventional commit format in title
- Fill out the PR template completely
- Link to related issues
- Provide context and motivation
- Include testing instructions
- Add screenshots for UI changes
- Keep PRs focused (< 400 lines ideal)
- Request specific reviewers

❌ **DON'T:**
- Create massive PRs (> 1000 lines)
- Skip the PR template
- Forget to link issues
- Mix unrelated changes
- Force push after review starts

### Example: Good Pull Request

```markdown
## Title
feat: implement user profile photo upload

## Description
This PR implements user profile photo upload as described in #42.

Changes include:
- Photo upload endpoint
- Image validation (size, format)
- S3 integration
- Thumbnail generation
- Frontend upload component

## Testing
1. Navigate to /profile
2. Click "Upload Photo"
3. Select image file (try JPG, PNG, GIF)
4. Verify photo appears
5. Try updating/removing photo

Tested on:
- Chrome 120
- Safari 17
- Mobile Safari

## Screenshots
[Before] [After]

## Related Issues
Closes #42
Depends on #43 (merged)

## Checklist
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Conventional commit format
- [x] Reviewed own code
```

### PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| **Tiny** | < 10 | < 5 min | ✅ Perfect for docs/config |
| **Small** | 10-100 | 10-20 min | ✅ Ideal size |
| **Medium** | 100-400 | 30-60 min | ✅ Acceptable |
| **Large** | 400-1000 | 1-2 hours | ⚠️ Consider splitting |
| **Huge** | > 1000 | > 2 hours | ❌ Definitely split |

### Review Response Time

**Target SLAs:**
- Initial review: Within 24 hours
- Follow-up review: Within 4 hours
- Emergency PRs: Within 1 hour

**As PR Author:**
- Respond to feedback within 24 hours
- Address all comments
- Re-request review after changes
- Don't take feedback personally

**As Reviewer:**
- Be constructive and kind
- Explain the "why" behind suggestions
- Approve if changes are minor
- Block only for critical issues

---

## Label Strategy

### Core Labels

**Type Labels (mutually exclusive):**
- `enhancement` - New features
- `bug` - Bug fixes
- `documentation` - Documentation changes
- `infrastructure` - Infrastructure/DevOps
- `research` - Investigations/spikes

**Priority Labels:**
- `priority:critical` - Drop everything
- `priority:high` - Next sprint
- `priority:medium` - This quarter
- `priority:low` - Someday/maybe

**Effort Labels:**
- `effort:small` - < 4 hours
- `effort:medium` - 1-3 days
- `effort:large` - > 3 days

**Status Labels:**
- `in-progress` - Currently being worked on
- `blocked` - Waiting on something
- `needs-review` - Ready for review
- `needs-info` - Needs more information

**Special Labels:**
- `good first issue` - For new contributors
- `help wanted` - Community help needed
- `pinned` - Never goes stale
- `security` - Security-related
- `breaking-change` - Breaking API change

### Label Color Coding

```bash
# Create labels with consistent colors
gh label create "priority:high" --color "d73a4a" --description "High priority"
gh label create "priority:medium" --color "fbca04" --description "Medium priority"
gh label create "priority:low" --color "0e8a16" --description "Low priority"

gh label create "effort:small" --color "c2e0c6" --description "< 4 hours"
gh label create "effort:medium" --color "bfdadc" --description "1-3 days"
gh label create "effort:large" --color "f9d0c4" --description "> 3 days"
```

### Label Best Practices

✅ **DO:**
- Apply labels when creating issues
- Use consistent label taxonomy
- Document label meanings
- Train team on label usage
- Review labels regularly

❌ **DON'T:**
- Create too many labels
- Use unclear label names
- Apply conflicting labels
- Change label meanings without notice

---

## Documentation

### Code Documentation

```python
# ✅ GOOD: Clear docstring
def sync_issues_to_todo(repo: str, labels: List[str]) -> bool:
    """
    Synchronize GitHub issues to TO-DO.md file.
    
    Args:
        repo: Repository in format 'owner/repo'
        labels: List of labels to filter issues
        
    Returns:
        True if sync successful, False otherwise
        
    Raises:
        GithubException: If API call fails
    """
    pass

# ❌ BAD: No documentation
def sync(r, l):
    pass
```

### Inline Comments

```python
# ✅ GOOD: Explains why, not what
# Use exponential backoff to handle rate limiting
for i in range(3):
    try:
        return api.call()
    except RateLimitException:
        time.sleep(2 ** i)

# ❌ BAD: States the obvious
# Loop 3 times
for i in range(3):
    pass
```

### README Standards

Every repository should have:

```markdown
# Project Name

Brief description

## Quick Start

```bash
# One-command installation
./setup.sh
```

## Documentation

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT
```

### Changelog Maintenance

```markdown
# Changelog

## [Unreleased]
### Added
- New feature description

### Changed
- Changed feature description

### Fixed
- Bug fix description

## [1.0.0] - 2024-01-15
### Added
- Initial release
```

---

## Team Collaboration

### Communication

**Issue Comments:**
- Keep team updated on progress
- Ask questions early
- Share blockers immediately
- Use @mentions to notify specific people

**PR Reviews:**
- Review within 24 hours
- Be specific in feedback
- Suggest improvements, don't demand
- Approve promptly if good

### Pair Programming

When pair programming:
- Use conventional commits
- Credit both authors
- Document decisions in commits

```bash
git commit -m "feat: implement feature (#42)

Co-authored-by: Jane Developer <jane@example.com>"
```

### Knowledge Sharing

- Document tribal knowledge
- Create runbooks for common tasks
- Share learnings in team meetings
- Maintain up-to-date onboarding docs

---

## Code Review

### What to Review

✅ **DO Review:**
- Code correctness
- Test coverage
- Error handling
- Performance implications
- Security concerns
- Code style consistency
- Documentation completeness

❌ **DON'T Bikeshed:**
- Minor style preferences (let linters handle it)
- Personal coding style
- Trivial naming debates

### Review Comments

✅ **GOOD:**
```
This could cause a race condition if two users update simultaneously.
Consider adding a database transaction or optimistic locking.
```

❌ **BAD:**
```
This is wrong.
```

### Review Levels

**🟢 Minor (Comment Only):**
- Style suggestions
- Optional improvements
- Nice-to-haves

**🟡 Major (Request Changes):**
- Logic errors
- Missing tests
- Incomplete implementation

**🔴 Blocking (Must Fix):**
- Security vulnerabilities
- Data corruption risks
- Breaking changes without migration

---

## Workflow Optimization

### Daily Workflow

```bash
# Morning routine
git pull origin main
gh issue list --assignee @me
python3 bin/sync-issues-to-todo.py

# During development
git checkout -b feature/issue-42-description
# ... make changes ...
git commit -m "feat: implement feature (#42)"
git push -u origin feature/issue-42-description
gh pr create --title "feat: implement feature" --body "Closes #42"

# End of day
python3 bin/capture-session.py
git push
```

### Weekly Workflow

```bash
# Monday: Plan week
gh issue list --label "priority:high"

# Friday: Review progress
python3 bin/generate-docs.py
git add docs/
git commit -m "docs: update weekly documentation"
```

### Automation Checklist

- [ ] Issues auto-sync to TO-DO.md
- [ ] Commits auto-link to issues
- [ ] PRs auto-validate
- [ ] Documentation auto-generates
- [ ] Stale issues auto-managed
- [ ] Labels auto-applied

---

## Metrics and KPIs

### Track These Metrics

**Velocity:**
- Issues closed per week
- PR merge rate
- Time to close issues

**Quality:**
- Bug rate
- PR revision count
- Test coverage

**Collaboration:**
- Review response time
- Issue comment activity
- PR approval time

### Example Metrics Tracking

```bash
# Issues closed this week
gh issue list --state closed --json closedAt \
  --jq '[.[] | select(.closedAt > "2024-01-01")] | length'

# Average PR review time
gh pr list --state merged --json reviewDecision,updatedAt,createdAt \
  --jq 'map(.updatedAt - .createdAt) | add / length'
```

---

## Common Pitfalls

### ❌ Anti-Patterns to Avoid

1. **Issue Hoarding**
   - Don't assign yourself 20 issues
   - Keep assignments to 2-3 active issues

2. **Commit Spamming**
   - Don't commit every character change
   - Squash related commits before PR

3. **PR Procrastination**
   - Don't sit on completed PRs
   - Create PR as soon as ready

4. **Review Ghosting**
   - Don't ignore review requests
   - Review within 24 hours

5. **Label Chaos**
   - Don't create duplicate labels
   - Follow label taxonomy

---

## Quick Reference

```
┌─────────────────────────────────────────────────────┐
│              IDD Best Practices Card                │
├─────────────────────────────────────────────────────┤
│ Issues:   Use templates, clear titles, link PRs    │
│ Commits:  Conventional format, link issues         │
│ PRs:      < 400 lines, fill template, link issues  │
│ Labels:   Consistent taxonomy, apply early         │
│ Reviews:  < 24 hours, be constructive              │
│ Docs:     Keep updated, use changelogs             │
└─────────────────────────────────────────────────────┘
```

---

**Follow these practices for smoother development! 🚀**
