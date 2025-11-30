from app.server import mcp_server

@mcp_server.tool
def email_tool(msg: str):
    return {"res": f"The email with message `{msg}` has been sent successfuly"}