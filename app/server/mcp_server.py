from fastmcp import FastMCP
from app.server.routes import register_tools

def create_mcp_server():
    mcp = FastMCP("Production MCP Server 🚀")
    register_tools(mcp)
    return mcp
