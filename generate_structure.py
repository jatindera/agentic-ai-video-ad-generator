import os

# ---------------------------
# Folder Structure Definition
# ---------------------------

structure = {
    ".": {
        "app": {
            "__init__.py": "",
            "core": {
                "__init__.py": "",
                "config.py": """from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str | None = None
    BING_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
""",
                "logging_config.py": "",
                "exceptions.py": "",
            },
            "server": {
                "__init__.py": "",
                "mcp_server.py": """from fastmcp import FastMCP
from app.server.routes import register_tools

def create_mcp_server():
    mcp = FastMCP("Production MCP Server 🚀")
    register_tools(mcp)
    return mcp
""",
                "routes.py": """from fastmcp import FastMCP

# Import tools
from app.tools.math_tools import add
from app.tools.google_search import google_search_tool
from app.tools.bing_search import bing_search_tool
from app.tools.weather_tool import weather_tool

def register_tools(mcp: FastMCP):
    mcp.add_tool(add)
    mcp.add_tool(google_search_tool)
    mcp.add_tool(bing_search_tool)
    mcp.add_tool(weather_tool)
""",
                "lifecycles.py": "",
            },
            "tools": {
                "__init__.py": "",
                "math_tools.py": """def add(a: int, b: int) -> int:
    '''Add two numbers'''
    return a + b
""",
                "google_search.py": """from app.services.google_service import google_search

async def google_search_tool(query: str):
    '''Search using Google'''
    return await google_search(query)
""",
                "bing_search.py": """from app.services.bing_service import bing_search

async def bing_search_tool(query: str):
    '''Search using Bing'''
    return await bing_search(query)
""",
                "weather_tool.py": """from app.services.weather_service import get_weather

async def weather_tool(city: str):
    '''Get weather for a city'''
    return await get_weather(city)
""",
                "http_client.py": "",
                "utils.py": "",
            },
            "models": {
                "__init__.py": "",
                "base.py": "",
                "search_models.py": "",
                "weather_models.py": "",
            },
            "services": {
                "__init__.py": "",
                "google_service.py": """import httpx
from app.core.config import settings

async def google_search(query: str):
    # Example placeholder implementation
    return { "query": query, "status": "google search stub" }
""",
                "bing_service.py": """import httpx
from app.core.config import settings

async def bing_search(query: str):
    # Example placeholder implementation
    return { "query": query, "status": "bing search stub" }
""",
                "weather_service.py": """import httpx
from app.core.config import settings

async def get_weather(city: str):
    return { "city": city, "status": "weather stub" }
""",
            },
            "utils": {
                "__init__.py": "",
                "caching.py": "",
                "retry.py": "",
                "rate_limit.py": "",
            },
        },
        "tests": {
            "__init__.py": "",
            "test_math_tools.py": """from app.tools.math_tools import add

def test_add():
    assert add(2, 3) == 5
""",
            "test_google_search.py": "",
            "test_weather_tool.py": "",
            "conftest.py": "",
        },
        ".env.example": "GOOGLE_API_KEY=\nBING_API_KEY=\nWEATHER_API_KEY=",
        "README.md": "# MCP Server\n\nProduction-ready MCP server scaffold.",
        "requirements.txt": "",
        "run.py": """from app.server.mcp_server import create_mcp_server

if __name__ == "__main__":
    mcp = create_mcp_server()
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
""",
    }
}

# ---------------------------
# Utility to Create Structure
# ---------------------------

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)

        # If value is dict → folder
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

        # If value is string → file
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


# ---------------------------
# Execute folder creation
# ---------------------------

if __name__ == "__main__":
    root = os.getcwd()
    create_structure(root, structure)
    print("📦 Project structure created successfully!")
