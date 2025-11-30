import asyncio
from fastmcp import Client, FastMCP
# HTTP server
client = Client("http://127.0.0.1:9000/mcp")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        tools = await client.list_tools()
        print(tools)
        
        # Execute operations
        hello_result = await client.call_tool("hello_tool", {"name": "Rishab"})
        print(hello_result.data['msg'])

        email_result = await client.call_tool("email_tool", {"msg": "You are awesome"})
        print(email_result.data['res'])


asyncio.run(main())