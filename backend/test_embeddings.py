import asyncio
from app.services.embedding_service import embedding_service

async def test():
    e = await embedding_service.generate_embedding("hello world")
    print("Embedding length =", len(e))

asyncio.run(test())