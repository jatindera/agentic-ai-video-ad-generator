from fastmcp import FastMCP

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
