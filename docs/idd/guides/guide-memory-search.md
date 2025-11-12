# Memory Search System - Usage Guide

**Script:** `bin/search-context.py`  
**Purpose:** Search and query captured development sessions and AI context memory

---

## Overview

The memory search system enables you to:
- Search full-text across all session files
- Filter by date ranges, issues, commit types
- Rank results by relevance
- Highlight matching context
- Output JSON for AI integration

---

## Installation

### Prerequisites

1. **Python 3.9+**
2. **AI context structure** with captured sessions
3. **Session files** in `.ai-context/memory/sessions/`

No additional dependencies required beyond Python standard library.

---

## Basic Usage

### Simple Text Search

```bash
# Search for "IDD"
python bin/search-context.py "IDD"

# Search for "session capture"
python bin/search-context.py "session capture"

# Search for "GitHub Actions"
python bin/search-context.py "GitHub Actions"
```

### Search with Filters

```bash
# Search last 7 days
python bin/search-context.py "automation" --date-range 7

# Search specific date
python bin/search-context.py "workflow" --date 2025-11-05

# Search date range
python bin/search-context.py "testing" --start-date 2025-11-01 --end-date 2025-11-05
```

### Filter by Issue

```bash
# Find sessions mentioning issue #15
python bin/search-context.py --issue 15

# Search text AND filter by issue
python bin/search-context.py "context" --issue 15
```

### Filter by Commit Type

```bash
# Find sessions with feat commits
python bin/search-context.py --type feat

# Find fix commits from last week
python bin/search-context.py --type fix --date-range 7

# Search text AND filter by type
python bin/search-context.py "bug" --type fix
```

---

## Advanced Features

### Case-Sensitive Search

```bash
# Case-sensitive search
python bin/search-context.py "IDD" --case-sensitive
```

### Regex Search

```bash
# Search with regex pattern
python bin/search-context.py "issue #\d+" --regex

# Find all PRs
python bin/search-context.py "PR #\d+" --regex

# Complex pattern
python bin/search-context.py "(feat|fix)\(" --regex
```

### JSON Output

```bash
# JSON format for AI integration
python bin/search-context.py "context" --format json

# JSON with filters
python bin/search-context.py --issue 15 --format json

# Pipe to jq for processing
python bin/search-context.py "IDD" --format json | jq '.total_matches'
```

### Hide Context Lines

```bash
# Show only matches without context
python bin/search-context.py "workflow" --no-context
```

---

## Command-Line Options

### Search Query

```
query              Search query (text or regex). Optional if using filters.
```

### Date Filters

```
--date-range N     Search last N days
--start-date DATE  Start date for search range (YYYY-MM-DD)
--end-date DATE    End date for search range (YYYY-MM-DD)
--date DATE        Search specific date only (YYYY-MM-DD)
```

### Content Filters

```
--issue N          Filter by issue number
--type TYPE        Filter by commit type (feat, fix, docs, refactor, test, chore, other)
```

### Search Options

```
--case-sensitive   Make search case-sensitive
--regex            Treat query as regex pattern
--no-context       Hide context lines in results
```

### Output Options

```
--format FORMAT    Output format: text (default) or json
--repo PATH        Path to git repository (default: current directory)
```

---

## Output Format

### Text Output (Default)

```
🔍 Found 1 session(s) with matches

================================================================================

1. Session: 2025-11-05
   File: 2025-11-05.md
   Matches: 13
   Relevance: 223
   Commits: 32
   Issues: #1, #2, #3, #5, #8
   Types: feat, fix, docs

   Match 1 (line 44):
      Context before...
   ➜  Matched line with highlighting
      Context after...

   Match 2 (line 52):
      ...

================================================================================
```

**Text Output Includes:**
- Session date and filename
- Match count and relevance score
- Session metadata (commits, issues, types)
- Up to 5 matches with context
- Highlighting on matched text

### JSON Output

```json
{
  "query_results": [
    {
      "date": "2025-11-05",
      "file": "2025-11-05.md",
      "match_count": 13,
      "relevance_score": 223,
      "metadata": {
        "commits": 32,
        "issues_referenced": [1, 2, 3, 5, 8],
        "commit_types": ["feat", "fix", "docs"],
        "files_changed": 138,
        "lines_changed": 10180
      },
      "matches": [
        {
          "line_number": 44,
          "line_content": "Matched line text",
          "context_before": ["Previous line"],
          "context_after": ["Next line"]
        }
      ]
    }
  ],
  "total_results": 1,
  "total_matches": 13
}
```

**JSON Output Includes:**
- All session metadata
- Up to 10 matches per session
- Context lines for each match
- Summary statistics

---

## Relevance Ranking

Results are ranked by relevance score based on:

1. **Match Count** (up to 100 points)
   - 10 points per match
   - Capped at 100

2. **Recency** (up to 50 points)
   - Recent sessions score higher
   - Score decreases with age

3. **Match in Headings** (20 points each)
   - Matches in markdown headings score higher
   - Indicates structural relevance

4. **Session Metadata** (variable points)
   - 5 points per referenced issue
   - 3 points per commit type

Higher scores appear first in results.

---

## Examples

### Daily Workflow Examples

#### Find Today's Work on a Feature

```bash
python bin/search-context.py "authentication" --date $(date +%Y-%m-%d)
```

#### Review Last Week's Fixes

```bash
python bin/search-context.py --type fix --date-range 7
```

#### Find All References to an Issue

```bash
python bin/search-context.py --issue 15
```

### Code Review Examples

#### Find All Feature Commits

```bash
python bin/search-context.py --type feat
```

#### Search for Specific File Changes

```bash
python bin/search-context.py "sync_issues_to_todo.py"
```

#### Find Documentation Updates

```bash
python bin/search-context.py --type docs --date-range 30
```

### AI Integration Examples

#### Get Context for AI Assistant

```bash
python bin/search-context.py "IDD implementation" --format json > context.json
```

#### Build Knowledge Base Query

```bash
python bin/search-context.py "certificate management" --format json | \
  jq '.query_results[0].matches[].line_content'
```

#### Find Related Sessions

```bash
# Find all sessions mentioning issue #15 and #16
for issue in 15 16; do
  echo "Issue #$issue:"
  python bin/search-context.py --issue $issue
done
```

---

## Use Cases

### 1. Code Archaeology

Find when a feature was implemented:

```bash
python bin/search-context.py "session capture" --type feat
```

### 2. Bug Investigation

Track down when a bug was introduced:

```bash
python bin/search-context.py "dashboard stats" --type fix
```

### 3. Documentation Review

Find all documentation changes:

```bash
python bin/search-context.py --type docs --date-range 30
```

### 4. Issue Tracking

See all work related to an issue:

```bash
python bin/search-context.py --issue 15 --format json
```

### 5. AI Context Building

Gather context for AI assistant:

```bash
# Get last week's context
python bin/search-context.py "infrastructure" --date-range 7 --format json
```

### 6. Project Retrospective

Review work over time:

```bash
# All feature work last month
python bin/search-context.py --type feat --date-range 30
```

---

## Integration with IDD Workflow

### Weekly Review

```bash
# Review last week's work
python bin/search-context.py --date-range 7
```

### Sprint Planning

```bash
# Find related past work
python bin/search-context.py "monitoring" --date-range 90
```

### Knowledge Transfer

```bash
# Export all sessions to JSON for new team member
python bin/search-context.py "" --format json > all-sessions.json
```

### AI Context Updates

```bash
# Update AI context with recent sessions
python bin/search-context.py --date-range 7 --format json > recent-context.json
```

---

## Performance

### Fast Search
- Indexes loaded once at startup
- Direct file reading (no database)
- Regex compiled once per search
- Typical search: < 1 second

### Memory Efficient
- Streams files line-by-line
- Limits matches per session (5 for text, 10 for JSON)
- Context lines extracted on-demand

### Scalability
- Handles hundreds of session files
- Date filtering reduces search space
- Index-based metadata filtering

---

## Troubleshooting

### "Sessions directory not found"

Ensure AI context structure exists:

```bash
ls -la .ai-context/memory/sessions/
```

If missing, run session capture first:

```bash
python bin/capture-session.py
```

### "No results found"

- Check that session files exist
- Verify search query spelling
- Try broader search terms
- Check date filters aren't too restrictive

### Slow Performance

- Use date filters to reduce search scope
- Use more specific search terms
- Consider regex complexity

### Regex Errors

Validate regex pattern:

```bash
python -c "import re; re.compile('your pattern here')"
```

---

## Tips & Best Practices

### Search Strategy

1. **Start Broad:** Use simple terms first
2. **Add Filters:** Narrow with date/issue/type
3. **Refine Query:** Use more specific terms
4. **Use Regex:** For complex patterns

### Query Patterns

```bash
# Good: Specific and focused
python bin/search-context.py "TO-DO.md dashboard"

# Better: Add filters
python bin/search-context.py "dashboard" --type feat --date-range 7

# Best: Combine query + filters
python bin/search-context.py "dashboard stats" --issue 10 --format json
```

### Daily Habits

1. **Morning:** Search yesterday's work
   ```bash
   python bin/search-context.py --date $(date -v-1d +%Y-%m-%d)
   ```

2. **End of Day:** Review today's commits
   ```bash
   python bin/search-context.py --date $(date +%Y-%m-%d)
   ```

3. **Weekly:** Review week's work
   ```bash
   python bin/search-context.py --date-range 7
   ```

---

## Future Enhancements

Planned improvements:

- [ ] Search across context snippets (not just sessions)
- [ ] Tag-based filtering
- [ ] Author filtering
- [ ] File path filtering
- [ ] Fuzzy search
- [ ] Search history
- [ ] Saved searches
- [ ] Web interface
- [ ] Interactive mode

---

## Support

**Documentation:** `.ai-context/README.md`  
**Related:** `docs/idd/session-capture-guide.md`  
**Issues:** [GitHub Issues](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/issues)  
**Roadmap:** `docs/idd/ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md`

---

**Last Updated:** 2025-11-05  
**Version:** 1.0  
**Script:** `bin/search-context.py`
