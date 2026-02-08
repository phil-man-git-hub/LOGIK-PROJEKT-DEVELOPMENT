# AI Diagnostics & Knowledge Base Guide

This guide explains how to leverage the integrated AI tools in LOGIK-PROJEKT for semantic search, real-time debugging, and automated context management.

## Components Overview

1.  **RAG (Retrieval-Augmented Generation)**: A semantic knowledge base containing documentation, source code, and historical session data.
2.  **MCP (Model Context Protocol) Server**: A standardized interface that allows AI agents to "talk" to the project, query the knowledge base, and check project status.
3.  **Live Diagnostics Bridge**: A real-time telemetry system that broadcasts application logs for immediate debugging by AI or humans.

---

## 1. RAG Knowledge Base

The RAG system uses ChromaDB to store vector embeddings of the repository.

### Initializing the Index
To process the codebase and documentation into the vector store:
```bash
./scripts/index_rag.py
```
*Note: This should be run after major documentation updates or code refactors.*

---

## 2. MCP Server

The MCP server provides tools that any compatible AI client (e.g., Claude Desktop) can use.

### Starting the Server
**Local (stdio) mode:**
```bash
./scripts/logik_projekt_mcp.py
```

**Background (SSE) mode (Port 54321):**
```bash
./scripts/logik_projekt_mcp.py --transport sse --port 54321 --background
```

### Available Tools
- `query_project_knowledge(query)`: Semantic search across the repo.
- `get_project_status()`: Reads the current `TO-DO.md`.
- `list_recent_sessions()`: Shows recent work history.
- `listen_to_live_logs(duration)`: Captures live application telemetry.

---

## 3. Live Diagnostics

LOGIK-PROJEKT broadcasts its internal state via UDP on port `54322`.

### Monitoring the App
To watch the application's "thoughts" in real-time:
```bash
./scripts/logik_debug_listener.py
```

### How it works
The `LogTransmitterHandler` in `src/app.py` intercepts standard Python `logging` calls and broadcasts them as JSON packets. This allows non-intrusive monitoring without blocking the UI thread.

---

## Example AI Workflow

1.  **Start the MCP Server** in the background.
2.  **Run LOGIK-PROJEKT** application.
3.  **Ask the AI**: *"What was the rationale behind the Flame bookmark logic implemented yesterday?"*
    - The AI uses `query_project_knowledge` to find the code and `list_recent_sessions` to find the relevant session summary.
4.  **Ask the AI to debug**: *"Listen to the logs for 10 seconds while I click the 'Create Project' button."*
    - The AI uses `listen_to_live_logs` to capture the telemetry and identifies why a specific step might be failing.
