---
description: Save an insight, session summary, or research note to the knowledge base.
---
1.  **Identify Content Type**:
    -   Ask the user (or determine from context) what type of file to create: `insight`, `session`, `research`, or `memory`.

2.  **Generate Filename**:
    -   Get current timestamp: `YYYY-MM-DD-HH-MM-SS`.
    -   Ask user for a `CATEGORY` (e.g., `auth`, `ui`, `database`) and a `BRIEF_DESCRIPTION`.
    -   Construct filename: `.gemini/antigravity/<type>s/<TIMESTAMP>-<CATEGORY>-<DESCRIPTION>.md`.

3.  **Write Content**:
    -   Create the file with the content provided by the user or summarized from the chat.

4.  **Update Git**:
    -   Ensure `.gitignore` still excludes `.gemini/` (just a safety check).
