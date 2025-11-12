# IDD Publication Guide

Guide for publishing and releasing your Issue-Driven Development system.

## Table of Contents

- [Release Preparation](#release-preparation)
- [Version Strategy](#version-strategy)
- [Release Checklist](#release-checklist)
- [GitHub Release](#github-release)
- [Release Assets](#release-assets)
- [Release Notes](#release-notes)
- [Post-Release](#post-release)

---

## Release Preparation

### Pre-Release Audit

Before creating a release, ensure your IDD system is ready:

```bash
# 1. Run all validations
python3 bin/validate-config.py idd-config.yml

# 2. Check for errors
gh workflow list
gh run list --limit 10

# 3. Verify documentation is current
ls -la docs/idd/

# 4. Test core functionality
python3 bin/sync-issues-to-todo.py
python3 bin/capture-session.py
```

### Documentation Review

Ensure all documentation is complete and accurate:

- [ ] README.md has current installation instructions
- [ ] QUICK_START.md is up to date
- [ ] SETUP_GUIDE.md covers all platforms
- [ ] TROUBLESHOOTING.md has recent solutions
- [ ] CUSTOMIZATION_GUIDE.md reflects current config
- [ ] BEST_PRACTICES.md is comprehensive
- [ ] ARCHITECTURE.md is accurate
- [ ] All code examples work

### Code Quality Check

```bash
# Check Python code
python3 -m py_compile bin/*.py

# Check shell scripts
shellcheck bin/*.sh

# Verify permissions
find bin/ -name "*.sh" -type f ! -perm -u+x

# Test scripts
./bin/setup-idd.sh --help
```

---

## Version Strategy

### Semantic Versioning

Follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH

1.0.0 → Initial release
1.1.0 → New features, backward compatible
1.1.1 → Bug fixes
2.0.0 → Breaking changes
```

### Version Numbering Guide

**MAJOR (X.0.0)** - Increment when:
- Breaking changes to configuration format
- Incompatible API changes
- Major workflow restructuring
- Removal of deprecated features

**MINOR (1.X.0)** - Increment when:
- New features added
- New workflows created
- New documentation
- Backward-compatible changes

**PATCH (1.0.X)** - Increment when:
- Bug fixes
- Documentation fixes
- Performance improvements
- No new features

### Release Tags

```bash
# Tag format: v{MAJOR}.{MINOR}.{PATCH}
git tag v1.0.0
git tag v1.1.0
git tag v2.0.0

# With annotation (recommended)
git tag -a v1.0.0 -m "Initial IDD release"

# Push tags
git push origin v1.0.0
git push origin --tags
```

---

## Release Checklist

### Pre-Release

- [ ] All open critical issues resolved
- [ ] All workflows passing
- [ ] Documentation reviewed and updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in all relevant files
- [ ] All tests passing
- [ ] Code reviewed by team member
- [ ] No security vulnerabilities

### Release Preparation

- [ ] Create release branch (optional)
  ```bash
  git checkout -b release/v1.0.0
  ```

- [ ] Update version references
  - [ ] Update version in `version/version.json`
  - [ ] Update version in documentation
  - [ ] Update version in examples

- [ ] Generate fresh documentation
  ```bash
  python3 bin/generate-docs.py
  ```

- [ ] Create changelog entry
  ```bash
  # Add to CHANGELOG.md under [Unreleased]
  ```

- [ ] Commit version bump
  ```bash
  git add .
  git commit -m "chore: bump version to v1.0.0"
  git push
  ```

- [ ] Create and push tag
  ```bash
  git tag -a v1.0.0 -m "Release v1.0.0"
  git push origin v1.0.0
  ```

### Release Creation

- [ ] Create GitHub release (see [GitHub Release](#github-release))
- [ ] Upload release assets (see [Release Assets](#release-assets))
- [ ] Publish release notes (see [Release Notes](#release-notes))
- [ ] Verify release appears in GitHub

### Post-Release

- [ ] Merge release branch to main (if used)
- [ ] Update development branch
- [ ] Announce release (see [SHARING_GUIDE.md](SHARING_GUIDE.md))
- [ ] Update project website/documentation
- [ ] Close milestone (if using milestones)
- [ ] Create next milestone

---

## GitHub Release

### Creating a Release via Web UI

1. **Navigate to Releases**
   - Go to your repository on GitHub
   - Click "Releases" in the right sidebar
   - Click "Draft a new release"

2. **Choose Tag**
   - Select existing tag or create new one
   - Format: `v1.0.0`
   - Target: `main` branch (or release branch)

3. **Release Title**
   - Format: `IDD v1.0.0 - Release Name`
   - Example: `IDD v1.0.0 - Initial Release`
   - Example: `IDD v1.1.0 - AI Context Enhancement`

4. **Release Description**
   - Use release notes template (see below)
   - Include highlights, changes, and upgrade notes

5. **Attach Assets**
   - Upload ZIP/tarball if created
   - Include documentation PDFs if relevant

6. **Publish**
   - Check "Set as latest release" for stable releases
   - Check "Set as pre-release" for beta/RC versions

### Creating a Release via CLI

```bash
# Create release with gh CLI
gh release create v1.0.0 \
  --title "IDD v1.0.0 - Initial Release" \
  --notes-file docs/release-notes/v1.0.0.md \
  --latest

# Upload assets
gh release upload v1.0.0 \
  idd-template-v1.0.0.zip \
  docs/IDD_Documentation.pdf

# Create pre-release
gh release create v1.1.0-beta.1 \
  --title "IDD v1.1.0 Beta 1" \
  --notes "Beta release for testing" \
  --prerelease
```

---

## Release Assets

### Template Package

Create a distributable package:

```bash
# Extract IDD template
./bin/extract-idd-template.sh

# This creates: idd-template-YYYYMMDD.zip
# Contents:
#   - .github/ (templates, workflows)
#   - bin/ (scripts)
#   - config/ (examples)
#   - docs/idd/ (documentation)
#   - idd-config.yml (template)
#   - requirements.txt
```

### Documentation Bundle

```bash
# Create documentation PDF (requires pandoc)
pandoc docs/idd/*.md \
  --pdf-engine=xelatex \
  -o IDD_Documentation.pdf

# Or create HTML bundle
mkdir -p idd-docs-html
for file in docs/idd/*.md; do
  pandoc "$file" -o "idd-docs-html/$(basename "$file" .md).html"
done
zip -r idd-docs-html.zip idd-docs-html/
```

### Quick Start Package

Create a minimal quickstart:

```bash
# Create quickstart directory
mkdir idd-quickstart
cd idd-quickstart

# Copy essential files
cp ../docs/idd/QUICK_START.md ./
cp ../idd-config.yml ./idd-config.template.yml
cp ../bin/setup-idd.sh ./
cp ../bin/validate-config.py ./
cp ../requirements.txt ./

# Create README
cat > README.md << 'EOF'
# IDD Quick Start Package

Get started with Issue-Driven Development in minutes!

## Installation

1. Run setup script:
   ```bash
   ./setup-idd.sh
   ```

2. Follow the prompts to configure your project.

## Documentation

- [Quick Start Guide](QUICK_START.md)
- [Full Documentation](https://github.com/your-org/your-repo/tree/main/docs/idd)

## Support

- [Issues](https://github.com/your-org/your-repo/issues)
- [Discussions](https://github.com/your-org/your-repo/discussions)
EOF

# Create ZIP
cd ..
zip -r idd-quickstart.zip idd-quickstart/
```

---

## Release Notes

### Template: Major Release

```markdown
# IDD v1.0.0 - Initial Release

We're excited to announce the first stable release of Issue-Driven Development (IDD)!

## 🎉 Highlights

- Complete issue-driven workflow automation
- AI-powered context capture and memory
- Comprehensive documentation system
- 7 GitHub Actions workflows
- 5 Python automation scripts
- 6 configuration examples

## ✨ What's New

### Core Features

- **Issue Templates**: Standardized bug reports, feature requests, and tasks
- **Automated Syncing**: Issues automatically sync to TO-DO.md
- **AI Context System**: Capture development sessions for AI assistants
- **Stale Management**: Automatically handle inactive issues
- **Documentation Generation**: Auto-generate changelogs and stats

### Workflows

- Issue validation and auto-labeling
- TO-DO.md synchronization
- AI context capture
- Stale issue management
- Documentation generation
- PR validation

### Documentation

- Quick start guide
- Comprehensive setup guide
- Troubleshooting guide
- Platform-specific notes (macOS, Linux, Windows)
- Customization guide
- Best practices
- Architecture documentation

## 📦 Installation

```bash
# Clone or extract template
gh repo clone your-org/idd-template

# Run setup
cd idd-template
./bin/setup-idd.sh
```

See [QUICK_START.md](docs/idd/QUICK_START.md) for detailed instructions.

## 🔄 Upgrade Notes

**First release** - No upgrade needed!

## 🐛 Bug Fixes

- N/A (initial release)

## 📚 Documentation

- [Quick Start](docs/idd/QUICK_START.md)
- [Setup Guide](docs/idd/SETUP_GUIDE.md)
- [Troubleshooting](docs/idd/TROUBLESHOOTING.md)
- [Customization](docs/idd/CUSTOMIZATION_GUIDE.md)
- [Best Practices](docs/idd/BEST_PRACTICES.md)
- [Architecture](docs/idd/ARCHITECTURE.md)

## 🙏 Acknowledgments

Thanks to all contributors who made this release possible!

## 📊 Stats

- **Lines of Code**: 10,000+
- **Documentation**: 15,000+ words
- **Workflows**: 7
- **Scripts**: 5
- **Templates**: 5
- **Examples**: 6

---

**Full Changelog**: https://github.com/your-org/your-repo/compare/...v1.0.0
```

### Template: Minor Release

```markdown
# IDD v1.1.0 - Enhanced AI Context

## ✨ New Features

- **Smart Context Filtering**: Automatically prioritize relevant context
- **Session Summaries**: Generate markdown summaries of work sessions
- **Privacy Modes**: New privacy settings for code capture

## 🔧 Improvements

- Faster issue synchronization (2x speed improvement)
- Better error messages in validation
- Improved documentation search

## 🐛 Bug Fixes

- Fixed issue sync with special characters (#123)
- Resolved timezone issues in session capture (#124)
- Fixed validation script on Windows (#125)

## 🔄 Upgrade Instructions

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python3 bin/validate-config.py idd-config.yml
```

No breaking changes! Your existing configuration will work as-is.

## 📚 Documentation Updates

- Added privacy mode guide
- Updated troubleshooting with new issues
- Improved Windows installation instructions

---

**Full Changelog**: https://github.com/your-org/your-repo/compare/v1.0.0...v1.1.0
```

### Template: Patch Release

```markdown
# IDD v1.0.1 - Bug Fixes

## 🐛 Bug Fixes

- Fixed sync failure with unicode characters (#130)
- Resolved Python 3.11 compatibility issue (#131)
- Fixed permission error in capture script (#132)

## 🔄 Upgrade Instructions

```bash
git pull origin main
# No configuration changes needed
```

## 📚 Documentation

- Fixed typos in setup guide
- Updated troubleshooting FAQ

---

**Full Changelog**: https://github.com/your-org/your-repo/compare/v1.0.0...v1.0.1
```

---

## Post-Release

### Announcement Checklist

After publishing the release:

- [ ] Post to project discussions
- [ ] Share on social media (see [SHARING_GUIDE.md](SHARING_GUIDE.md))
- [ ] Update documentation website
- [ ] Send email to users (if applicable)
- [ ] Post in relevant communities
- [ ] Update badges in README

### Monitoring

Track release adoption:

```bash
# Watch release downloads
gh release view v1.0.0

# Monitor issues related to release
gh issue list --label "v1.0.0"

# Check for bug reports
gh issue list --label "bug" --state open
```

### Hotfix Process

If critical bugs are found:

1. Create hotfix branch
   ```bash
   git checkout -b hotfix/v1.0.1 v1.0.0
   ```

2. Fix the bug and commit
   ```bash
   git commit -m "fix: critical bug in sync script"
   ```

3. Update version and tag
   ```bash
   git tag v1.0.1
   ```

4. Create emergency release
   ```bash
   gh release create v1.0.1 --title "v1.0.1 - Critical Hotfix"
   ```

5. Merge back to main
   ```bash
   git checkout main
   git merge hotfix/v1.0.1
   ```

---

## Release Schedule Recommendations

### Versioning Cadence

**Major Releases** (X.0.0):
- Frequency: 1-2 per year
- Planning: 3-6 months
- Breaking changes allowed

**Minor Releases** (1.X.0):
- Frequency: Monthly or bi-monthly
- Planning: 2-4 weeks
- New features, backward compatible

**Patch Releases** (1.0.X):
- Frequency: As needed (days to weeks)
- Planning: Immediate for critical bugs
- Bug fixes only

### Release Calendar Example

```
Q1 2024:
- Jan: v1.1.0 (new features)
- Feb: v1.1.1 (bug fixes)
- Mar: v1.2.0 (new features)

Q2 2024:
- Apr: v1.2.1 (bug fixes)
- May: v1.3.0 (new features)
- Jun: v2.0.0 (major release)
```

---

## Automation

### Automated Release Creation

```yaml
# .github/workflows/release.yml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Release Notes
        id: notes
        run: |
          python3 bin/generate-release-notes.py > release-notes.md
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: release-notes.md
          draft: false
          prerelease: false
      
      - name: Create Template Package
        run: |
          ./bin/extract-idd-template.sh
      
      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./idd-template-*.zip
          asset_name: idd-template.zip
          asset_content_type: application/zip
```

---

## Quick Reference

```
┌──────────────────────────────────────────────────────┐
│           IDD Release Process Card                   │
├──────────────────────────────────────────────────────┤
│ 1. Update CHANGELOG.md                               │
│ 2. Bump version in version.json                      │
│ 3. Commit: "chore: bump version to vX.Y.Z"           │
│ 4. Tag: git tag -a vX.Y.Z -m "Release vX.Y.Z"        │
│ 5. Push: git push origin vX.Y.Z                      │
│ 6. Create GitHub release                             │
│ 7. Upload assets                                     │
│ 8. Announce release                                  │
└──────────────────────────────────────────────────────┘
```

---

**Ready to publish? Check out [SHARING_GUIDE.md](SHARING_GUIDE.md) for community outreach!**
