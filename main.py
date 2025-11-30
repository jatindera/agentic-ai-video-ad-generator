from app.server import mcp_server

# Import ALL tool modules so decorators execute
import app.tools


if __name__ == "__main__":
    mcp_server.run(transport="http", host="0.0.0.0", port=9000, path="/mcp")