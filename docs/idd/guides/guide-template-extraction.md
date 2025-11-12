# IDD Template Extraction Guide

## Overview

This guide documents how to extract the Issue-Driven Development (IDD) system from this repository into a reusable template that can be applied to any project.

## Template Repository Structure

The extracted template should have the following structure:

```
github-idd-template/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01_feature.yml
│   │   ├── 02_bug.yml
│   │   ├── 03_documentation.yml
│   │   ├── 04_infrastructure.yml
│   │   └── 05_research.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── workflows/
│   │   ├── issue-to-todo-sync.yml
│   │   ├── auto-label.yml
│   │   ├── pr-validation.yml
│   │   ├── commit-to-issue-link.yml
│   │   ├── stale-management.yml
│   │   ├── smart-labeling.yml
│   │   └── auto-docs.yml
│   └── dependabot.yml (optional)
├── .ai-context/
│   ├── README.md
│   ├── config.json
│   ├── sessions/
│   ├── search_index/
│   ├── context_snapshots/
│   └── insights/
├── bin/
│   ├── sync-issues-to-todo.py
│   ├── capture-session.py
│   ├── search-context.py
│   ├── retrieve-context.py
│   └── generate-docs.py
├── docs/
│   ├── idd/
│   │   ├── README.md
│   │   ├── QUICK_START.md
│   │   ├── SETUP_GUIDE.md
│   │   ├── CUSTOMIZATION_GUIDE.md
│   │   ├── ARCHITECTURE.md
│   │   └── BEST_PRACTICES.md
│   └── examples/
│       ├── sample-issue.md
│       ├── sample-pr.md
│       └── sample-workflow.md
├── config/
│   └── idd-config.template.yml
├── tests/
│   └── test_idd_scripts.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Components to Extract

### 1. GitHub Issue Templates

**Source Location:** `.github/ISSUE_TEMPLATE/`

**Files to Extract:**
- `01_feature.yml` - Feature request template
- `02_bug.yml` - Bug report template
- `03_documentation.yml` - Documentation task template
- `04_infrastructure.yml` - Infrastructure task template
- `05_research.yml` - Research task template

**Parameterization Needs:**
- Label names (may vary by project)
- Project-specific sections
- Custom fields

**Example Configuration:**
```yaml
# config/idd-config.template.yml
issue_templates:
  feature:
    labels: ["enhancement", "needs-triage"]
    custom_fields: []
  bug:
    labels: ["bug", "needs-triage"]
    auto_assign: true
```

### 2. GitHub Workflows

**Source Location:** `.github/workflows/`

**Files to Extract:**

1. **issue-to-todo-sync.yml** (52 lines)
   - Syncs GitHub issues to TO-DO.md
   - Dependencies: bin/sync-issues-to-todo.py
   - Parameterization: File paths, labels to track

2. **auto-label.yml** (48 lines)
   - Automatically labels issues based on content
   - Dependencies: None (uses GitHub Actions API)
   - Parameterization: Label mappings, keywords

3. **pr-validation.yml** (56 lines)
   - Validates PR titles and descriptions
   - Dependencies: None
   - Parameterization: Validation rules

4. **commit-to-issue-link.yml** (162 lines)
   - Links commits to issues automatically
   - Dependencies: GitHub API
   - Parameterization: Comment templates

5. **stale-management.yml** (125 lines)
   - Manages stale issues and PRs
   - Dependencies: actions/stale
   - Parameterization: Timeouts, labels, messages

6. **smart-labeling.yml** (227 lines)
   - Intelligent label detection and application
   - Dependencies: GitHub API, Python script
   - Parameterization: Label rules, patterns

7. **auto-docs.yml** (80 lines)
   - Generates documentation automatically
   - Dependencies: bin/generate-docs.py
   - Parameterization: Output locations, formats

**Common Parameterization:**
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  PROJECT_NAME: ${PROJECT_NAME}
  TODO_FILE_PATH: ${TODO_FILE_PATH}
  LABELS_TO_TRACK: ${LABELS_TO_TRACK}
```

### 3. Python Scripts

**Source Location:** `bin/`

**Files to Extract:**

1. **sync-issues-to-todo.py** (314 lines)
   - Syncs issues to markdown file
   - Dependencies: PyGithub, python-dotenv
   - Parameterization: Repository, file paths, labels

2. **capture-session.py** (600+ lines)
   - Captures development sessions
   - Dependencies: GitPython, PyGithub
   - Parameterization: Directory structure, formats

3. **search-context.py** (610+ lines)
   - Full-text search of AI context
   - Dependencies: Custom search index
   - Parameterization: Index locations, search fields

4. **retrieve-context.py** (638+ lines)
   - Intelligent context retrieval
   - Dependencies: All AI context scripts
   - Parameterization: Context assembly rules

5. **generate-docs.py** (246 lines)
   - Automated documentation generation
   - Dependencies: GitPython
   - Parameterization: Output formats, templates

**requirements.txt:**
```
PyGithub>=2.1.1
python-dotenv>=1.0.0
GitPython>=3.1.40
```

### 4. AI Context System

**Source Location:** `.ai-context/`

**Structure to Extract:**
```
.ai-context/
├── README.md                 # System documentation
├── config.json              # Configuration
├── sessions/                # Development sessions
│   └── .gitkeep
├── search_index/            # Search index
│   └── .gitkeep
├── context_snapshots/       # Context snapshots
│   └── .gitkeep
└── insights/                # Extracted insights
    └── .gitkeep
```

**config.json Template:**
```json
{
  "project": {
    "name": "${PROJECT_NAME}",
    "repository": "${REPOSITORY}",
    "description": "${DESCRIPTION}"
  },
  "capture": {
    "auto_capture": true,
    "capture_commits": true,
    "capture_issues": true,
    "capture_prs": true
  },
  "search": {
    "index_sessions": true,
    "index_snapshots": true,
    "index_insights": true
  },
  "retention": {
    "max_sessions": 100,
    "max_age_days": 90
  }
}
```

### 5. Documentation

**Documentation to Create:**

1. **README.md** - Template overview and quick start
2. **QUICK_START.md** - 5-minute setup guide
3. **SETUP_GUIDE.md** - Detailed installation instructions
4. **CUSTOMIZATION_GUIDE.md** - How to customize for your project
5. **ARCHITECTURE.md** - System architecture and design
6. **BEST_PRACTICES.md** - IDD best practices

## Parameterization Strategy

### Configuration File: `config/idd-config.yml`

```yaml
# IDD Configuration Template
# Copy this to your repository root and customize

project:
  name: "Your Project Name"
  repository: "owner/repo"
  main_branch: "main"
  
files:
  todo_file: "TO-DO.md"
  changelog: "docs/CHANGELOG.md"
  stats: "docs/PROJECT_STATS.md"
  
labels:
  # Labels to track in TO-DO.md
  track:
    - "enhancement"
    - "bug"
    - "documentation"
  
  # Auto-labeling rules
  auto_label:
    feature:
      keywords: ["feature", "add", "implement"]
      labels: ["enhancement"]
    bug:
      keywords: ["bug", "error", "fix"]
      labels: ["bug"]
    docs:
      keywords: ["document", "docs", "guide"]
      labels: ["documentation"]
  
  # Stale issue management
  stale:
    days_before_stale: 60
    days_before_close: 7
    exempt_labels: ["pinned", "security"]
    stale_label: "stale"

workflows:
  # Enable/disable specific workflows
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: true
  smart_labeling: true
  auto_docs: true

ai_context:
  enabled: true
  auto_capture: true
  retention_days: 90
  max_sessions: 100

documentation:
  auto_generate: true
  changelog_enabled: true
  stats_enabled: true
  update_readme: true
```

### Setup Script: `bin/setup-idd.sh`

```bash
#!/bin/bash
# Setup script for IDD template

set -e

echo "🚀 Setting up Issue-Driven Development..."

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 required"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "❌ GitHub CLI required"; exit 1; }

# Get project information
read -p "Project name: " PROJECT_NAME
read -p "GitHub repository (owner/repo): " REPOSITORY
read -p "Main branch [main]: " MAIN_BRANCH
MAIN_BRANCH=${MAIN_BRANCH:-main}

# Create configuration
echo "📝 Creating configuration..."
sed -e "s/\${PROJECT_NAME}/$PROJECT_NAME/g" \
    -e "s/\${REPOSITORY}/$REPOSITORY/g" \
    -e "s/\${MAIN_BRANCH}/$MAIN_BRANCH/g" \
    config/idd-config.template.yml > idd-config.yml

# Create .ai-context structure
echo "📁 Creating AI context directories..."
mkdir -p .ai-context/{sessions,search_index,context_snapshots,insights}

# Set up Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure GitHub
echo "🔐 Configuring GitHub..."
gh auth status || gh auth login

# Create initial TO-DO.md
echo "📋 Creating TO-DO.md..."
cat > TO-DO.md << 'EOF'
# Project TO-DO List

*This file is automatically synchronized with GitHub Issues*

## 🎯 Active Issues

No active issues yet.

## ✅ Completed Issues

No completed issues yet.

---
*Last updated: $(date)*
EOF

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review idd-config.yml and customize as needed"
echo "2. Commit the configuration: git add . && git commit -m 'feat: set up IDD'"
echo "3. Push to GitHub: git push"
echo "4. GitHub Actions workflows will activate automatically"
echo ""
echo "📚 Documentation: docs/idd/README.md"
```

## Usage Instructions

### For Template Maintainers

1. **Extract Components:**
   ```bash
   # Create new repository
   mkdir github-idd-template
   cd github-idd-template
   git init
   
   # Copy structure
   mkdir -p .github/ISSUE_TEMPLATE .github/workflows
   mkdir -p bin docs/idd config tests
   mkdir -p .ai-context/{sessions,search_index,context_snapshots,insights}
   
   # Copy files (from source repository)
   cp -r SOURCE_REPO/.github/ISSUE_TEMPLATE/* .github/ISSUE_TEMPLATE/
   cp -r SOURCE_REPO/.github/workflows/* .github/workflows/
   cp SOURCE_REPO/.github/PULL_REQUEST_TEMPLATE.md .github/
   cp SOURCE_REPO/bin/*.py bin/
   cp SOURCE_REPO/requirements.txt .
   ```

2. **Parameterize Scripts:**
   - Replace hardcoded values with config file references
   - Add environment variable support
   - Create configuration templates

3. **Create Documentation:**
   - Write comprehensive README
   - Create setup guides
   - Add examples
   - Document customization options

4. **Test Template:**
   - Create test repository
   - Run setup script
   - Verify all workflows work
   - Test with different configurations

### For Template Users

1. **Clone Template:**
   ```bash
   git clone https://github.com/YOUR_ORG/github-idd-template.git
   cd your-project
   ```

2. **Run Setup:**
   ```bash
   chmod +x bin/setup-idd.sh
   ./bin/setup-idd.sh
   ```

3. **Customize Configuration:**
   - Edit `idd-config.yml`
   - Update labels and workflows
   - Adjust automation settings

4. **Activate:**
   ```bash
   git add .
   git commit -m "feat: set up IDD"
   git push
   ```

## File Inventory

### Total Files to Extract: 32 files

**GitHub Configuration (9 files):**
- 5 issue templates
- 1 PR template
- 7 workflow files
- 1 dependabot.yml (optional)

**Python Scripts (5 files):**
- sync-issues-to-todo.py
- capture-session.py
- search-context.py
- retrieve-context.py
- generate-docs.py

**Documentation (8+ files):**
- README.md
- QUICK_START.md
- SETUP_GUIDE.md
- CUSTOMIZATION_GUIDE.md
- ARCHITECTURE.md
- BEST_PRACTICES.md
- Multiple examples

**Configuration (3 files):**
- idd-config.template.yml
- requirements.txt
- .gitignore

**AI Context (4 files):**
- .ai-context/README.md
- .ai-context/config.json
- Directory structure (.gitkeep files)
- Documentation

**Setup Tools (2 files):**
- setup-idd.sh
- test_idd_scripts.py

## Metrics

**Total Lines of Code to Extract:** ~7,200+ lines
- Workflows: ~750 lines
- Scripts: ~2,600 lines
- Templates: ~500 lines
- Documentation: ~3,000+ lines
- Configuration: ~350 lines

**Estimated Extraction Time:** 2-3 hours
**Estimated Documentation Time:** 2-3 hours
**Total Week 4 Time:** 6-8 hours

## Success Criteria

Template is successful when:

1. ✅ Can be cloned to any repository
2. ✅ Setup script runs without errors
3. ✅ All workflows activate correctly
4. ✅ Scripts work with configuration
5. ✅ Documentation is comprehensive
6. ✅ Customization is straightforward
7. ✅ Examples are clear and helpful
8. ✅ No hardcoded repository-specific values
9. ✅ Tests pass on fresh repository
10. ✅ Community can adopt easily

## Next Steps

After completing this template extraction:

1. **Week 4.2:** Create comprehensive setup guide
2. **Week 4.3:** Build configuration & customization system
3. **Week 4.4:** Publish and share template

## Related Documents

- [IDD Roadmap](./ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md)
- [Architecture Overview](./architecture/)
- [Implementation Insights](./insights/)
- [Best Practices](./BEST_PRACTICES.md) (to be created)
