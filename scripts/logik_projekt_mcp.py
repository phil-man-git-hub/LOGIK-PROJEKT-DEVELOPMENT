#!/usr/bin/env python3
import os
import sys

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api.core.mcp.server import server

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the LOGIK-PROJEKT MCP Server")
    parser.add_argument("--reindex", action="store_true", help="Re-index the repository before starting")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transport type (default: stdio)")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport (default: 8000)")
    parser.add_argument("--background", action="store_true", help="Run the server in the background")
    
    args = parser.parse_args()

    if args.reindex:
        from api.core.rag.rag_manager import RAGManager
        print("Re-indexing repository...")
        rag_manager = RAGManager()
        rag_manager.initialize_index()
        print("Re-indexing complete.")

    if args.background and args.transport == "sse":
        import subprocess
        import sys
        # Remove --background to avoid recursion
        new_args = [a for a in sys.argv if a != "--background"]
        # Use nohup to keep it running
        log_file = "logs/mcp_server.log"
        os.makedirs("logs", exist_ok=True)
        print(f"Starting MCP server in background. Logging to {log_file}")
        # Set port in env using FastMCP's expected prefix
        env = os.environ.copy()
        env["FASTMCP_PORT"] = str(args.port)
        env["FASTMCP_HOST"] = "0.0.0.0"
        with open(log_file, "a") as f:
            subprocess.Popen([sys.executable] + new_args, stdout=f, stderr=f, start_new_session=True, env=env)
        sys.exit(0)

    # If sse and not background, set env for current process
    if args.transport == "sse":
        os.environ["FASTMCP_PORT"] = str(args.port)
        os.environ["FASTMCP_HOST"] = "0.0.0.0"

    # Run the MCP server
    server.run(transport=args.transport)
