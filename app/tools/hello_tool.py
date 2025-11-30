from app.server import mcp_server

@mcp_server.tool
def hello_tool(name: str):
    return {"msg": f"hello, {name}"}