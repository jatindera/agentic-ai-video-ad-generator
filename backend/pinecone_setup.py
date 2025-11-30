"""
Simple Python script to create a Pinecone index named 'prompt-examples',
following the same configuration style as your PineconeService class.
"""

from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------------
# 1. Read API Key
# ------------------------------------------------------------------------------
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY environment variable is not set")

# ------------------------------------------------------------------------------
# 2. Initialize Pinecone Client
# ------------------------------------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "prompt-examples"

# ------------------------------------------------------------------------------
# 3. Create Index if Not Exists
# ------------------------------------------------------------------------------
existing = [idx["name"] for idx in pc.list_indexes()]

if index_name not in existing:
    print(f"🟦 Creating Pinecone index '{index_name}' ...")

    pc.create_index(
        name=index_name,
        dimension=3072,               # Same as text-embedding-3-large
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

    print("🟩 Index created successfully!")
else:
    print(f"🟩 Index '{index_name}' already exists.")

# ------------------------------------------------------------------------------
# 4. Connect to the Index
# ------------------------------------------------------------------------------
index = pc.Index(index_name)
print(f"✅ Connected to index '{index_name}'")

# ------------------------------------------------------------------------------
# 5. OPTIONAL: Example Upsert (matches your metadata format)
# ------------------------------------------------------------------------------
# dummy embedding (3072 floats)
dummy_embedding = [0.001] * 3072  

dummy_metadata = {
    "business_type": "Smart Speakers",
    "ad_style": "Cinematic",
    "tone": "Friendly",
    "target_audience": "Young Adults",
    "tags": ["audio", "tech", "gadgets"]
}

example_id = "example-001"

print(f"🟦 Upserting sample vector with ID={example_id} ...")

index.upsert(
    vectors=[
        {
            "id": example_id,
            "values": dummy_embedding,
            "metadata": dummy_metadata
        }
    ]
)

print("🟩 Sample upsert complete.")
print("🎉 Setup done!")