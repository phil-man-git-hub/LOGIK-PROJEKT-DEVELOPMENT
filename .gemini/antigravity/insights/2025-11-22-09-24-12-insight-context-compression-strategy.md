# Insight: Context Compression & The "Second Brain" Strategy

## What is Context Compression?
Large Language Models (LLMs) like Gemini have a fixed "Context Window" — a limit on how much text (code, chat history, documents) they can "see" at one time.

When a conversation gets too long, the system must "compress" the context. This usually means:
1.  **Summarizing** older parts of the chat.
2.  **Dropping** very old messages entirely.
3.  **Truncating** large files that were previously read.

**The Risk:** When context is compressed, the AI "forgets" specific details, instructions, or decisions made earlier in the session.

## How Our Workflow Mitigates This
The `.gemini/antigravity` directory structure acts as an **External Long-Term Memory** that is immune to context compression.

### The Strategy
1.  **Offloading**: Instead of relying on the chat history (which gets compressed), we offload important facts to files in `memory/` and `insights/`.
2.  **Retrieval**: When the AI needs to recall something, it doesn't look at its own fading memory; it reads the persistent file.
3.  **Checkpoints**: By writing session summaries to `sessions/`, we create "save points" that allow the AI to get up to speed instantly, even if the actual chat history is completely wiped.

### Workflow Adjustment
To actively provision for context compression:
*   **Aggressive Summarization**: Don't wait for the end of a session. If we reach a complex conclusion, write it to `insights/` immediately.
*   **Reference over Repetition**: Instead of re-explaining a task, refer to a `to-dos/` file.
*   **"Refresh" Reads**: If the AI seems confused or forgetful, ask it to re-read specific files in `.gemini/antigravity/`.
