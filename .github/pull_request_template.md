# Pull Request Template for LOGIK-PROJEKT

## Title
<!--
  - Use format: [TYPE] Short description (#issue-number)
  - Example: [FEATURE] Add desktop app automation (#42)
-->

## Linked Issue
<!--
  - Link to the relevant issue using: Closes #issue-number
  - Example: Closes #42
-->

## Description
<!--
  - Briefly describe the purpose and context of this PR.
  - Include any relevant background, motivation, or design decisions.
-->

## Checklist
- [ ] PR title follows required format
- [ ] Linked to a relevant issue (Closes #...)
- [ ] All new and updated code is documented
- [ ] Tests added or updated (if applicable)
- [ ] CI checks pass (lint, tests, workflows)
- [ ] Changelog and release notes updated
- [ ] No large, unrelated changes (PR is focused)
- [ ] All reviewers added

## Additional Notes
<!--
  - Add any extra context, screenshots, or migration notes here.
--><!-- 
Thank you for your Pull Request! 
Please fill out this template to help reviewers understand your changes.
Delete sections that aren't applicable to your PR.
-->

## Description
<!-- Provide a clear and concise description of what this PR does -->



## Closes
<!-- Link the issue(s) this PR addresses. Use "Closes #123" to auto-close issues when merged -->

Closes #


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



## Screenshots/Demos
<!-- If applicable, add screenshots, GIFs, or demo videos to help explain your changes -->

<details>
<summary>Click to view screenshots</summary>

<!-- Add your screenshots here -->

</details>


## Documentation
<!-- Check all that apply -->

- [ ] Code is self-documenting with clear comments
- [ ] README.md updated (if applicable)
- [ ] Documentation added/updated in `docs/` directory
- [ ] Inline documentation/comments added
- [ ] No documentation changes needed


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


## Dependencies
<!-- List any dependencies this PR has on other PRs, issues, or external factors -->

- Depends on: 
- Blocks: 
- Related to: 


## Migration/Deployment Notes
<!-- If applicable, describe any special steps needed for deployment or migration -->

### Pre-deployment
- 

### Post-deployment
- 


## Rollback Plan
<!-- Describe how to rollback these changes if issues arise after deployment -->



## Additional Context
<!-- Add any other context, concerns, or notes about the PR here -->



## Post-Merge Tasks
<!-- List any tasks that need to be done after this PR is merged -->

- [ ] Update related documentation
- [ ] Notify relevant team members
- [ ] Monitor for issues
- [ ] Close related issues (if not auto-closed)
- [ ] Update TO-DO.md task status


---

<!-- 
IDD Workflow Reference:
- Branch naming: feature/issue-N-description or fix/issue-N-description
- Commit format: type(scope): description
- Always link to issues with "Closes #N" or "Implements #N"
- Keep PRs focused on a single issue when possible
-->
