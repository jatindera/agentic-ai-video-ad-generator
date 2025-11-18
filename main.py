from app.server.mcp_server import create_mcp_server

if __name__ == "__main__":
    mcp = create_mcp_server()
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
