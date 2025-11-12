# Pull Request Template Guide

## Overview

The Pull Request (PR) template provides a standardized structure for all pull requests in the Issue-Driven Development workflow. It ensures consistency, improves code review quality, and maintains proper documentation of changes.

**Template Location:** `.github/pull_request_template.md`

## Purpose

The PR template serves multiple purposes:

1. **Standardization** - Ensures all PRs have consistent structure and information
2. **Documentation** - Captures the context and rationale behind changes
3. **Quality Assurance** - Provides checklists to verify testing and review completeness
4. **Automation Integration** - Links PRs to issues for automatic workflow management
5. **Knowledge Transfer** - Helps reviewers and future maintainers understand changes

## Template Structure

### 1. Description Section

```markdown
## Description
<!-- Provide a clear and concise description of what this PR does -->
```

**Purpose:** High-level summary of what this PR accomplishes.

**Best Practices:**
- Start with a one-sentence summary
- Explain the "why" not just the "what"
- Keep it concise but informative
- Use clear, non-technical language when possible

**Example:**
```markdown
## Description

This PR implements automated backup rotation for the monitoring system. 
The current backup system was filling up disk space with indefinite retention.
This change adds a configurable retention policy with automatic cleanup of old backups.
```

### 2. Closes Section

```markdown
## Closes
<!-- Link the issue(s) this PR addresses. Use "Closes #123" to auto-close issues when merged -->

Closes #
```

**Purpose:** Links the PR to GitHub issues and triggers automatic issue closure upon merge.

**Important Keywords:**
- `Closes #N` - Closes the issue when PR is merged
- `Fixes #N` - Same as Closes (alternative keyword)
- `Resolves #N` - Same as Closes (alternative keyword)
- `Implements #N` - Links but doesn't auto-close (use in commits)

**Best Practices:**
- Always link to at least one issue
- Use multiple "Closes #N" lines for PRs that address multiple issues
- One issue per line for clarity
- Verify issue numbers are correct before submitting

**Examples:**
```markdown
Closes #42
```

```markdown
Closes #15
Closes #23
Closes #31
```

### 3. Type of Change Section

```markdown
## Type of Change
<!-- Check the relevant option(s) -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style/formatting update
- [ ] ♻️ Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test addition or update
- [ ] 🔧 Configuration change
- [ ] 🏗️ Infrastructure/tooling change
```

**Purpose:** Categorizes the PR for easier review and changelog generation.

**Best Practices:**
- Check all applicable types (multiple are allowed)
- Be honest about breaking changes - they require special attention
- Consider semantic versioning implications:
  - Bug fixes → patch version bump
  - Features → minor version bump
  - Breaking changes → major version bump

### 4. Changes Made Section

```markdown
## Changes Made
<!-- Describe the changes in detail. Use categories if helpful -->

### Added
- 

### Changed
- 

### Removed
- 

### Fixed
- 
```

**Purpose:** Provides detailed list of all changes, organized by category.

**Best Practices:**
- Use bullet points for readability
- Be specific about file and function names
- Group related changes together
- Remove unused category subsections
- Use present tense ("Add feature X" not "Added feature X")

**Example:**
```markdown
## Changes Made

### Added
- New `backup_rotation.sh` script in `bin/` directory
- Configuration file `backup-rotation.conf` with retention policies
- Cron job for daily backup cleanup
- Documentation in `docs/backup-rotation.md`

### Changed
- Updated `backup.sh` to log backup creation timestamps
- Modified `monitoring.conf` to include backup status checks

### Fixed
- Corrected file permission issues in backup directory
- Fixed race condition in backup lock file handling
```

### 5. Testing Performed Section

```markdown
## Testing Performed
<!-- Describe the testing you've done to validate your changes -->

### Test Environment
- OS: 
- Environment: 

### Test Cases
- [ ] Tested locally
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Tested on target platform(s)

### Test Results
<!-- Describe what you tested and the results -->
```

**Purpose:** Documents testing approach and results to verify changes work correctly.

**Best Practices:**
- Be specific about test environment (OS, versions, configuration)
- Describe manual test procedures
- Include test output or logs if relevant
- Document any test failures and how they were resolved
- Test on actual target platforms when possible

**Example:**
```markdown
## Testing Performed

### Test Environment
- OS: Rocky Linux 9.5
- Environment: lima.projekt.lab (monitoring server)
- Backup storage: NFS mount on tango.projekt.lab

### Test Cases
- [x] Tested locally on development VM
- [x] Unit tests added for retention policy calculation
- [x] Integration tests with actual backup files
- [x] Manual testing completed over 7-day period
- [x] Tested on production monitoring server (dry-run mode)

### Test Results
- Created 100 test backup files spanning 90 days
- Verified retention policy correctly identifies files to keep/remove
- Tested edge cases: leap years, timezone changes, missing files
- Dry-run on production showed 247 old backups would be removed (23GB saved)
- All unit tests pass (15/15)
- Integration test suite passes (8/8)
```

### 6. Screenshots/Demos Section

```markdown
## Screenshots/Demos
<!-- If applicable, add screenshots, GIFs, or demo videos to help explain your changes -->

<details>
<summary>Click to view screenshots</summary>

<!-- Add your screenshots here -->

</details>
```

**Purpose:** Visual aids to help reviewers understand UI changes or complex behavior.

**When to Use:**
- UI/UX changes
- New dashboards or monitoring views
- Configuration screen updates
- Visual bug fixes
- Complex workflows

**Best Practices:**
- Use collapsible `<details>` sections to keep PRs readable
- Include before/after screenshots for UI changes
- Annotate screenshots to highlight important changes
- Use GIFs for demonstrating workflows or interactions
- Keep image sizes reasonable (compress large images)

### 7. Documentation Section

```markdown
## Documentation
<!-- Check all that apply -->

- [ ] Code is self-documenting with clear comments
- [ ] README.md updated (if applicable)
- [ ] Documentation added/updated in `docs/` directory
- [ ] Inline documentation/comments added
- [ ] No documentation changes needed
```

**Purpose:** Ensures proper documentation accompanies code changes.

**Best Practices:**
- Update documentation as part of the same PR (not later)
- Don't check "self-documenting" without actually adding comments
- Update README.md for user-facing changes
- Add/update docs in `docs/` for complex features
- Check "No documentation changes needed" only for truly trivial changes

### 8. Checklist Section

```markdown
## Checklist
<!-- Verify you've completed these items -->

### Before Requesting Review
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors
- [ ] I have tested my changes thoroughly
- [ ] My commits follow the conventional commit format (feat/fix/docs/etc)
- [ ] I have linked this PR to the related issue(s)
- [ ] I have updated the TO-DO.md if applicable

### For Reviewers
- [ ] Code quality is acceptable
- [ ] Tests are adequate and passing
- [ ] Documentation is clear and complete
- [ ] Changes align with project goals
- [ ] No security concerns identified
- [ ] Ready to merge
```

**Purpose:** Quality assurance checklist for both authors and reviewers.

**Best Practices:**
- Complete the "Before Requesting Review" section before marking PR as ready
- Leave "For Reviewers" section unchecked - reviewers will check these
- Take each item seriously - don't just check boxes
- If you can't check something, explain why in comments
- Use draft PRs if checklist isn't complete yet

### 9. Dependencies Section

```markdown
## Dependencies
<!-- List any dependencies this PR has on other PRs, issues, or external factors -->

- Depends on: 
- Blocks: 
- Related to: 
```

**Purpose:** Documents relationships between PRs and issues.

**Best Practices:**
- Use "Depends on" for PRs that must be merged first
- Use "Blocks" for issues/PRs that are waiting on this one
- Use "Related to" for loosely connected work
- Link to specific PRs/issues with #N notation

**Example:**
```markdown
## Dependencies

- Depends on: #35 (backup infrastructure must be in place first)
- Blocks: #38 (monitoring integration waiting for this)
- Related to: #28 (similar approach used for log rotation)
```

### 10. Migration/Deployment Notes Section

```markdown
## Migration/Deployment Notes
<!-- If applicable, describe any special steps needed for deployment or migration -->

### Pre-deployment
- 

### Post-deployment
- 
```

**Purpose:** Documents special deployment procedures or migration steps.

**When to Use:**
- Database schema changes
- Configuration file updates
- Service restarts required
- Data migrations
- Breaking changes

**Example:**
```markdown
## Migration/Deployment Notes

### Pre-deployment
- Backup current backup directory structure
- Stop cron jobs temporarily: `systemctl stop crond`
- Verify sufficient disk space for retention policy run

### Post-deployment
- Review and update `backup-rotation.conf` with desired retention days
- Run initial cleanup in dry-run mode: `backup_rotation.sh --dry-run`
- Restart cron service: `systemctl start crond`
- Monitor first automated run in logs
```

### 11. Rollback Plan Section

```markdown
## Rollback Plan
<!-- Describe how to rollback these changes if issues arise after deployment -->
```

**Purpose:** Documents how to undo changes if problems occur in production.

**Best Practices:**
- Always have a rollback plan for production changes
- Test rollback procedure before deployment when possible
- Document data restoration if applicable
- Include commands or scripts to execute rollback

**Example:**
```markdown
## Rollback Plan

If issues arise:
1. Revert to previous Git commit: `git revert abc123`
2. Remove new cron job: `crontab -e` and delete backup rotation line
3. Restore any accidentally deleted backups from `/backup/archive/`
4. Restart monitoring services: `systemctl restart librenms`

No data loss risk - deletion script preserves backups in archive directory.
```

### 12. Additional Context Section

```markdown
## Additional Context
<!-- Add any other context, concerns, or notes about the PR here -->
```

**Purpose:** Catch-all section for anything not covered elsewhere.

**When to Use:**
- Known limitations or caveats
- Future improvements planned
- Alternative approaches considered
- Performance implications
- Security considerations

### 13. Post-Merge Tasks Section

```markdown
## Post-Merge Tasks
<!-- List any tasks that need to be done after this PR is merged -->

- [ ] Update related documentation
- [ ] Notify relevant team members
- [ ] Monitor for issues
- [ ] Close related issues (if not auto-closed)
- [ ] Update TO-DO.md task status
```

**Purpose:** Tracks follow-up actions after merge.

**Best Practices:**
- Create tracking issues for substantial post-merge work
- Set reminders for monitoring periods
- Document who should be notified
- Don't forget to update TO-DO.md (will be automated later)

## Usage Instructions

### Creating a New Pull Request

#### Via GitHub Web UI

1. Push your feature branch to GitHub
2. Navigate to the repository on GitHub
3. Click "Pull requests" → "New pull request"
4. Select your feature branch
5. GitHub will automatically populate the PR description with the template
6. Fill in all sections of the template
7. Delete any sections that aren't applicable
8. Submit the PR

#### Via GitHub CLI

```bash
# Create PR with template (it will auto-populate)
gh pr create --title "Your PR Title" --web

# Or create PR directly with filled template
gh pr create \
  --title "Implement backup rotation" \
  --body "$(cat your-pr-description.md)" \
  --base main \
  --head feature/issue-42-backup-rotation
```

### Reviewing a Pull Request

As a reviewer, focus on:

1. **Description Clarity** - Can you understand what and why?
2. **Issue Linking** - Is this PR properly linked to issue(s)?
3. **Change Scope** - Are changes focused and relevant?
4. **Testing** - Is testing adequate and well-documented?
5. **Documentation** - Are docs updated appropriately?
6. **Code Quality** - Does code meet project standards?
7. **Security** - Any security concerns?

Use the "For Reviewers" checklist as your guide.

## Integration with IDD Workflow

The PR template integrates with the Issue-Driven Development workflow at these points:

### 1. Issue → PR Linking

```markdown
Closes #42
```

This creates bidirectional linking between issues and PRs.

### 2. Branch Naming Convention

Referenced in template footer:
```markdown
Branch naming: feature/issue-N-description or fix/issue-N-description
```

### 3. Commit Message Format

Referenced in checklist:
```markdown
- [ ] My commits follow the conventional commit format (feat/fix/docs/etc)
```

### 4. TO-DO.md Synchronization

Checklist items:
```markdown
- [ ] I have updated the TO-DO.md if applicable
- [ ] Update TO-DO.md task status (post-merge)
```

(Will be automated in Phase 1, Task 3)

## Automation Opportunities

Future automation planned for Phase 1:

### Auto-label PRs Based on Type

```yaml
# .github/workflows/pr-labeler.yml
# When PR is opened, auto-apply labels based on "Type of Change" checkboxes
```

### Auto-update TO-DO.md

```yaml
# .github/workflows/todo-sync.yml
# When PR is merged, update TO-DO.md with completion status
```

### PR Size Validator

```yaml
# .github/workflows/pr-size-check.yml
# Warn if PR exceeds recommended size (500 lines changed)
```

### Checklist Enforcer

```yaml
# .github/workflows/pr-checklist.yml
# Ensure all "Before Requesting Review" items are checked
```

## Best Practices

### For PR Authors

1. **Fill Out Completely** - Don't skip sections without good reason
2. **Be Specific** - Vague descriptions slow down reviews
3. **Self-Review First** - Review your own PR before requesting others
4. **Keep PRs Focused** - One issue per PR when possible
5. **Test Thoroughly** - Test on actual target environment
6. **Update Documentation** - Don't postpone docs to "later"
7. **Link to Issues** - Always use "Closes #N" for issue linking
8. **Use Draft PRs** - Mark as draft if not ready for review

### For Reviewers

1. **Be Constructive** - Focus on improvements, not criticism
2. **Ask Questions** - Seek understanding before judging
3. **Check Tests** - Verify tests actually test the changes
4. **Consider Security** - Think about security implications
5. **Test Locally** - Pull and test complex changes yourself
6. **Approve Explicitly** - Use GitHub's approval feature
7. **Respond Promptly** - Don't leave PRs hanging

### For Everyone

1. **Small PRs** - Aim for PRs under 500 lines changed
2. **Clear Titles** - Use descriptive PR titles
3. **Communication** - Discuss complex changes before PR
4. **Iteration** - Expect and embrace feedback
5. **Documentation** - Treat docs as first-class citizens

## Examples

### Example 1: Bug Fix PR

```markdown
## Description

Fixes a race condition in the backup lock file handling that caused occasional
backup failures when multiple backup jobs started simultaneously.

## Closes

Closes #156

## Type of Change

- [x] 🐛 Bug fix (non-breaking change that fixes an issue)

## Changes Made

### Fixed
- Added atomic lock file creation using `flock` in `bin/backup.sh`
- Implemented retry logic with exponential backoff (max 3 retries)
- Added proper lock cleanup in error paths

## Testing Performed

### Test Environment
- OS: Rocky Linux 9.5
- Environment: lima.projekt.lab

### Test Cases
- [x] Tested locally with simulated concurrent backups
- [x] Manual testing completed
- [x] Tested on production (dry-run mode)

### Test Results
- Ran 50 concurrent backup attempts - all succeeded with proper lock handling
- No lock file leaks detected
- Average wait time: 2.3 seconds when lock is held

## Documentation

- [x] Inline documentation/comments added
- [x] No documentation changes needed

## Checklist

### Before Requesting Review
- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] My changes generate no new warnings or errors
- [x] I have tested my changes thoroughly
- [x] My commits follow the conventional commit format
- [x] I have linked this PR to the related issue(s)

## Post-Merge Tasks

- [x] Monitor backup logs for 48 hours post-deployment
- [x] Update TO-DO.md task status
```

### Example 2: Feature PR

```markdown
## Description

Implements automated backup rotation with configurable retention policies.
The monitoring server was running out of disk space due to indefinite backup retention.
This adds a cleanup script that runs daily and removes backups older than the configured retention period.

## Closes

Closes #42

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)
- [x] 📝 Documentation update

## Changes Made

### Added
- New `backup_rotation.sh` script in `bin/` directory
- Configuration file `/etc/backup-rotation.conf` with retention policies
- Cron job for daily backup cleanup at 2 AM
- Comprehensive documentation in `docs/backup-rotation.md`
- Unit tests in `tests/test_backup_rotation.sh`

### Changed
- Updated `backup.sh` to log creation timestamps in metadata
- Modified monitoring dashboard to show backup retention stats

## Testing Performed

### Test Environment
- OS: Rocky Linux 9.5
- Environment: lima.projekt.lab (monitoring server)
- Backup storage: NFS mount on tango.projekt.lab (5TB available)

### Test Cases
- [x] Tested locally on development VM
- [x] Unit tests added/updated (15 tests, all passing)
- [x] Integration tests with 100 test backup files
- [x] Manual testing completed over 7-day period
- [x] Tested on production server (dry-run mode)

### Test Results
- Successfully deleted 247 old backups in dry-run (23GB freed)
- Retention policy calculation verified for various date scenarios
- Edge cases tested: leap years, timezone changes, missing metadata files
- All unit tests pass: 15/15
- Integration tests pass: 8/8

## Screenshots/Demos

<details>
<summary>Click to view dashboard screenshot</summary>

![Backup Dashboard](screenshots/backup-dashboard.png)

Shows new "Retention Status" widget with cleanup statistics.

</details>

## Documentation

- [x] Code is self-documenting with clear comments
- [x] README.md updated with backup rotation section
- [x] Documentation added in `docs/backup-rotation.md`
- [x] Inline documentation/comments added

## Checklist

### Before Requesting Review
- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] My changes generate no new warnings or errors
- [x] I have tested my changes thoroughly
- [x] My commits follow the conventional commit format
- [x] I have linked this PR to the related issue(s)
- [x] I have updated the TO-DO.md

## Dependencies

- Related to: #28 (log rotation uses similar approach)

## Migration/Deployment Notes

### Pre-deployment
1. Backup current backup directory: `tar -czf backup-snapshot.tar.gz /backup/librenms/`
2. Stop cron temporarily: `systemctl stop crond`
3. Verify 30GB+ disk space available for retention policy run

### Post-deployment
1. Review and customize `/etc/backup-rotation.conf`:
   - Set `RETENTION_DAYS=30` (or desired value)
   - Verify `BACKUP_DIR=/backup/librenms`
2. Run initial cleanup in dry-run mode:
   ```bash
   /usr/local/bin/backup_rotation.sh --dry-run
   ```
3. Review output, then run actual cleanup:
   ```bash
   /usr/local/bin/backup_rotation.sh
   ```
4. Restart cron: `systemctl start crond`
5. Verify cron job installed: `crontab -l | grep backup_rotation`
6. Monitor first automated run in `/var/log/backup-rotation.log`

## Rollback Plan

If issues arise:
1. Disable cron job:
   ```bash
   crontab -e  # Comment out backup_rotation line
   ```
2. Restore accidentally deleted backups from archive:
   ```bash
   rsync -av /backup/archive/ /backup/librenms/
   ```
3. Revert to previous version:
   ```bash
   git revert <commit-hash>
   ```

**Safety:** Script moves files to archive directory before deletion, providing 7-day recovery window.

## Additional Context

### Future Improvements
- Add Slack/email notifications for cleanup operations
- Implement intelligent retention (keep daily for 7d, weekly for 30d, monthly for 1y)
- Add backup integrity verification before deletion
- Create web UI for retention policy configuration

### Performance Notes
- Cleanup of 247 files took 23 seconds (SSD storage)
- Minimal CPU usage (<5% during cleanup)
- No impact on running backups (separate process)

## Post-Merge Tasks

- [x] Update backup documentation in wiki
- [x] Notify infrastructure team of new retention policies
- [x] Monitor disk space for 7 days post-deployment
- [x] Update TO-DO.md task status
- [ ] Create follow-up issue for intelligent retention (#TBD)
```

## Common Mistakes to Avoid

1. **Empty Sections** - Delete sections that don't apply, don't leave them empty
2. **Missing Issue Links** - Always link with "Closes #N"
3. **Unchecked Checklists** - Don't submit with empty checkboxes
4. **Vague Descriptions** - Be specific about what and why
5. **No Testing Info** - Always document how you tested
6. **Forgetting Documentation** - Update docs in same PR
7. **Too Large PRs** - Break large changes into smaller PRs
8. **No Rollback Plan** - Always have a way to undo changes

## Tips for Success

1. **Use the Template** - It's there for a reason
2. **Be Thorough** - Better to over-document than under-document
3. **Think of Reviewers** - Make their job easier
4. **Test Before PR** - Don't use PR as your testing ground
5. **Respond to Feedback** - Engage with reviewers promptly
6. **Keep History Clean** - Squash commits if needed
7. **Update Template** - Suggest improvements to the template itself

## Getting Help

- **Template Issues**: Open issue with label `documentation`
- **IDD Questions**: See `docs/idd/README.md`
- **Review Guidelines**: See `docs/idd/architecture/system-design.md`
- **Examples**: Browse closed PRs for real-world examples

## Related Documentation

- [Issue Templates Guide](issue-templates-guide.md)
- [IDD Roadmap](../ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md)
- [IDD System Architecture](../architecture/system-design.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub PR Documentation](https://docs.github.com/en/pull-requests)

---

**Last Updated:** November 5, 2025  
**Version:** 1.0.0  
**Status:** Active
