import os
import asyncio
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings
from mcp.server.fastmcp import FastMCP
from api.core.rag.rag_manager import RAGManager

class MCPSettings(BaseSettings):
    """Configuration for the LOGIK-PROJEKT MCP Server."""
    server_name: str = "LOGIK-PROJEKT Server"
    rag_root_dir: str = Field(default_factory=os.getcwd)
    rag_storage_path: str = ".chroma_db"
    
    class Config:
        env_prefix = "LOGIK_MCP_"

class LogikProjektMCPServer:
    """Encapsulates the MCP server logic and tools."""
    
    def __init__(self):
        self.settings = MCPSettings()
        # Initialize FastMCP with settings from pydantic
        self.mcp = FastMCP(
            self.settings.server_name,
            host="0.0.0.0", # Allow external connections for SSE
            port=int(os.environ.get("FASTMCP_PORT", 8000))
        )
        self.rag_manager = RAGManager(
            root_dir=self.settings.rag_root_dir,
            storage_path=self.settings.rag_storage_path
        )
        self._register_tools()

    def _register_tools(self):
        """Registers tools with the FastMCP instance."""
        
        @self.mcp.tool()
        async def query_project_knowledge(query: str, n_results: int = 5) -> str:
            """
            Search the LOGIK-PROJEKT repository documentation, sessions, and scripts 
            for relevant information using semantic RAG.
            """
            return self.rag_manager.query_context(query, n_results=n_results)

        @self.mcp.tool()
        async def get_project_status() -> str:
            """
            Retrieves the current status of the project from TO-DO.md.
            """
            todo_path = os.path.join(os.getcwd(), "TO-DO.md")
            if os.path.exists(todo_path):
                with open(todo_path, "r") as f:
                    return f.read()
            return "TO-DO.md not found."

        @self.mcp.tool()
        async def list_recent_sessions(limit: int = 5) -> str:
            """
            Lists the most recent development session summaries.
            """
            sessions_dir = ".gemini/antigravity/sessions"
            if not os.path.exists(sessions_dir):
                return "Sessions directory not found."
            
            files = sorted(os.listdir(sessions_dir), reverse=True)[:limit]
            return "\n".join(files)

        @self.mcp.tool()
        async def listen_to_live_logs(duration: int = 5) -> str:
            """
            Listens to the live application diagnostic stream for a specified duration (in seconds).
            Returns the captured log entries. Useful for real-time debugging of the running app.
            """
            import socket
            import time
            import json
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.2)
            try:
                sock.bind(('127.0.0.1', 54322))
            except OSError:
                sock.close()
                return "Error: Could not bind to diagnostic port. Is another listener active?"
            
            captured = []
            start_time = time.time()
            
            while time.time() - start_time < duration:
                try:
                    data, addr = sock.recvfrom(4096)
                    line = data.decode('utf-8')
                    try:
                        record = json.loads(line)
                        level = record.get("level", "INFO")
                        msg = record.get("message", "")
                        mod = record.get("module", "")
                        captured.append(f"[{level}] {mod}: {msg}")
                    except:
                        captured.append(line)
                except socket.timeout:
                    await asyncio.sleep(0.1)
                    continue
            
            sock.close()
            
            if not captured:
                return f"No logs captured in {duration}s. Ensure LOGIK-PROJEKT is running."
            
            return "\n".join(captured)

    def run(self, transport: str = "stdio"):
        """Starts the MCP server with the specified transport."""
        if transport == "sse":
            print(f"Starting MCP SSE server")
            self.mcp.run(transport="sse")
        else:
            self.mcp.run(transport="stdio")

# Entry point for module-level access
server = LogikProjektMCPServer()
mcp = server.mcp

if __name__ == "__main__":
    server.run()
