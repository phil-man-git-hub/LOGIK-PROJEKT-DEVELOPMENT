# Context Retrieval System - Usage Guide

**Script:** `bin/retrieve-context.py`  
**Purpose:** Intelligent context assembly from multiple sources for AI assistants

---

## Overview

The context retrieval system intelligently assembles relevant context from multiple sources:
- **Active context** - Current work state
- **Sessions** - Recent development sessions
- **Snippets** - Topic-specific knowledge bases
- **Decisions** - Architecture decisions and quick decisions

It provides:
- Relevance scoring based on query/topic
- Recency weighting for time-sensitive context
- Token management to fit AI context limits
- Multiple modes for different use cases
- Smart truncation and summarization

---

## Installation

### Prerequisites

1. **Python 3.9+**
2. **AI context structure** (from issue #15)
3. **Captured sessions** (from issue #17)
4. **Context snippets** (optional, enhances results)

No additional dependencies required.

---

## Basic Usage

### Get Focused Context on a Topic

```bash
python bin/retrieve-context.py --topic "IDD implementation"
```

### Get Comprehensive Recent Context

```bash
python bin/retrieve-context.py --mode comprehensive --days 7
```

### Get Context for Specific Issue

```bash
python bin/retrieve-context.py --issue 15
```

### Limited Tokens for Smaller AI Models

```bash
python bin/retrieve-context.py --topic "testing" --max-tokens 4000
```

---

## Context Modes

### Focused Mode (Default for Specific Queries)

```bash
python bin/retrieve-context.py --topic "session capture" --mode focused
```

**Characteristics:**
- Top 3 highest-scoring sources only
- Optimized for specific questions
- Lower token usage
- Best for: Direct questions, specific topics

### Broad Mode (Default)

```bash
python bin/retrieve-context.py --mode broad
```

**Characteristics:**
- Multiple sources with summarization
- Balanced coverage and depth
- Moderate token usage
- Best for: General context, exploratory queries

### Comprehensive Mode

```bash
python bin/retrieve-context.py --mode comprehensive --max-tokens 16000
```

**Characteristics:**
- All relevant sources
- Maximum coverage
- High token usage
- Best for: Deep research, full understanding

---

## Command-Line Options

### Context Selection

```
--topic, --query TEXT      Topic or search query for relevance scoring
--issue N                  Focus on specific issue number
--topics TOPIC [TOPIC...]  Specific context snippet topics to include
```

### Context Mode

```
--mode MODE               Context assembly mode: focused, broad, comprehensive
                         (default: broad)
--days N                  Number of days back for sessions (default: 7)
--max-tokens N            Maximum tokens in output (default: 8000)
```

### Output Options

```
--no-metadata             Exclude metadata header from output
--output, -o FILE         Write output to file instead of stdout
--repo PATH               Path to git repository (default: current directory)
```

---

## Output Format

### Metadata Header

```markdown
# AI Context Assembly

**Mode:** broad
**Generated:** 2025-11-05T12:39:02
**Sources:** 3
**Total Tokens:** ~1788
**Query:** IDD implementation
**Issue:** #15
```

### Source Sections

Each source includes:
- **Type** - active-context, session, snippet, decision
- **Metadata** - Date, relevance, recency scores
- **Token count** - Estimated tokens
- **Score** - Combined relevance/recency score
- **Content** - Full or truncated content

---

## Scoring System

### Relevance Score (0-1)

Based on query match density:
- Counts query occurrences in content
- Includes individual query words (weighted 0.5x)
- Normalized by content length
- Capped at 1.0

### Recency Score (0-1)

Exponential decay over time:
- Score = e^(-days/30)
- Recent = 1.0, 30 days ago = 0.37, 90 days ago = 0.05
- Only applies to dated content (sessions)

### Combined Score

For sessions:
```
combined_score = (relevance * 0.6) + (recency * 0.4)
```

For snippets:
```
score = relevance * 0.8
```

For active context:
```
score = 1.0  (always highest priority)
```

For decisions:
```
score = 0.7  (fixed moderate priority)
```

---

## Token Management

### Token Estimation

Simple heuristic: **1 token ≈ 4 characters**

This approximation works well for:
- English text
- Code with reasonable formatting
- Markdown documents

### Token Limits

Default limits by mode:
- **Focused:** 8,000 tokens (fits most AI contexts)
- **Broad:** 8,000 tokens (balanced)
- **Comprehensive:** 8,000 tokens (can increase with `--max-tokens`)

### Smart Truncation

When content exceeds limits:
1. Tries to truncate at paragraph boundaries
2. Keeps at least 70% of target length
3. Adds "[... truncated ...]" marker
4. Preserves most relevant parts (top-scored)

---

## Examples

### Daily Workflow Examples

#### Morning: Get Yesterday's Context

```bash
python bin/retrieve-context.py --days 1
```

#### Start Work on Issue

```bash
python bin/retrieve-context.py --issue 15 --mode focused
```

#### Research a Topic

```bash
python bin/retrieve-context.py --topic "certificate management" --mode comprehensive
```

### AI Integration Examples

#### Provide Context to AI Assistant

```bash
# Save context to file
python bin/retrieve-context.py --topic "IDD" -o context.md

# Or pipe directly
python bin/retrieve-context.py --topic "monitoring" | pbcopy
```

#### Limited Context for Smaller Models

```bash
# GPT-3.5 (4K context)
python bin/retrieve-context.py --topic "testing" --max-tokens 3000

# Claude Instant (9K context)
python bin/retrieve-context.py --topic "infrastructure" --max-tokens 7000
```

#### Comprehensive Context for Large Models

```bash
# GPT-4 (32K context)
python bin/retrieve-context.py --mode comprehensive --max-tokens 20000

# Claude 2 (100K context)
python bin/retrieve-context.py --mode comprehensive --max-tokens 50000
```

### Development Examples

#### Review Recent Work

```bash
python bin/retrieve-context.py --days 7
```

#### Find Context for Bug Fix

```bash
python bin/retrieve-context.py --topic "dashboard stats" --mode focused
```

#### Prepare for Code Review

```bash
python bin/retrieve-context.py --issue 10 --mode broad
```

---

## Use Cases

### 1. AI Pair Programming

Provide AI assistant with relevant context:

```bash
# Working on monitoring
python bin/retrieve-context.py --topic "monitoring" -o context.md

# Then in your AI conversation:
# "Using the context in context.md, help me implement LibreNMS alerts"
```

### 2. Code Review Preparation

Get full context for PR review:

```bash
python bin/retrieve-context.py --issue 15 --mode comprehensive
```

### 3. Knowledge Transfer

Export context for new team member:

```bash
python bin/retrieve-context.py --days 30 --mode comprehensive \
  -o onboarding-context.md
```

### 4. Documentation Writing

Gather context for documentation:

```bash
python bin/retrieve-context.py --topics idd-implementation infrastructure
```

### 5. Bug Investigation

Find related historical context:

```bash
python bin/retrieve-context.py --topic "sync script" --days 30
```

### 6. Sprint Planning

Review recent work and context:

```bash
python bin/retrieve-context.py --days 14 --mode broad
```

---

## Advanced Usage

### Multiple Topics

```bash
python bin/retrieve-context.py --topics idd-implementation infrastructure monitoring
```

### Custom Token Limits

```bash
# Very small (mobile AI)
python bin/retrieve-context.py --topic "quick summary" --max-tokens 1000

# Very large (GPT-4 Turbo)
python bin/retrieve-context.py --mode comprehensive --max-tokens 100000
```

### No Metadata (Clean Output)

```bash
python bin/retrieve-context.py --topic "testing" --no-metadata
```

### Save to Specific Location

```bash
python bin/retrieve-context.py --issue 15 -o ~/Desktop/issue-15-context.md
```

---

## Integration Patterns

### With AI Chat Systems

```bash
#!/bin/bash
# ai-chat-with-context.sh

TOPIC="$1"
CONTEXT=$(python bin/retrieve-context.py --topic "$TOPIC" --no-metadata)

# Pass to AI (example with hypothetical CLI)
echo "$CONTEXT" | ai-chat --system "You have access to this project context"
```

### With VS Code

Add to your tasks.json:

```json
{
  "label": "Get AI Context",
  "type": "shell",
  "command": "python",
  "args": [
    "bin/retrieve-context.py",
    "--topic",
    "${input:topic}",
    "-o",
    "ai-context.md"
  ],
  "inputs": [
    {
      "id": "topic",
      "type": "promptString",
      "description": "Enter topic for context"
    }
  ]
}
```

### With GitHub Copilot

```bash
# Generate context file that Copilot can see
python bin/retrieve-context.py --topic "current task" -o .copilot-context.md

# Add to .gitignore
echo ".copilot-context.md" >> .gitignore
```

---

## Performance

### Speed
- **Fast:** < 1 second for focused mode
- **Moderate:** 1-2 seconds for broad mode
- **Slower:** 2-5 seconds for comprehensive with many sources

### Memory
- Streams content line-by-line
- Minimal memory footprint
- Scales to hundreds of sources

### Accuracy
- Relevance scoring validated
- Token estimation ~10% accurate
- Truncation preserves meaning

---

## Troubleshooting

### "AI context directory not found"

Ensure AI context structure exists:

```bash
ls -la .ai-context/
```

If missing, run issue #15 setup.

### Low Relevance Scores

Try:
- More specific query terms
- Broader search (remove filters)
- Different query phrasing
- Check if content exists for topic

### Too Many/Few Sources

Adjust mode:
- **Too many:** Use `--mode focused`
- **Too few:** Use `--mode comprehensive` or increase `--days`

### Token Limit Exceeded

Reduce token limit or use focused mode:

```bash
python bin/retrieve-context.py --topic "xyz" --max-tokens 4000 --mode focused
```

---

## Tips & Best Practices

### Query Formulation

**Good queries:**
- Specific: "session capture implementation"
- Technical: "GitHub Actions workflow"
- Issue-focused: "dashboard stats bug"

**Less effective:**
- Too broad: "code"
- Single word: "test"
- Vague: "stuff"

### Mode Selection

- **Focused:** Know what you're looking for
- **Broad:** Exploring or researching
- **Comprehensive:** Deep dive or documentation

### Token Budget

**Conservative (4K models):**
```bash
--max-tokens 3000  # Leave room for conversation
```

**Moderate (8-16K models):**
```bash
--max-tokens 8000  # Default, works well
```

**Generous (32K+ models):**
```bash
--max-tokens 20000  # Deep context
```

---

## Future Enhancements

Planned improvements:

- [ ] Semantic similarity scoring (embeddings)
- [ ] User feedback learning
- [ ] Context caching
- [ ] Incremental updates
- [ ] Multi-repository support
- [ ] Custom source weights
- [ ] Tag-based filtering
- [ ] Time-of-day patterns

---

## Support

**Documentation:** `.ai-context/README.md`  
**Related:** 
- `docs/idd/session-capture-guide.md`
- `docs/idd/memory-search-guide.md`

**Issues:** [GitHub Issues](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/issues)  
**Roadmap:** `docs/idd/ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md`

---

**Last Updated:** 2025-11-05  
**Version:** 1.0  
**Script:** `bin/retrieve-context.py`
