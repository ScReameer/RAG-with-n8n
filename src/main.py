import uvicorn
import requests
import asyncio
from functools import partial
from fastapi import FastAPI
from pydantic import BaseModel
from encoder import encode, load_model

load_model()

app = FastAPI()


class EmbedRequest(BaseModel):
    """
    Request model for embedding
    """
    text: str


@app.post("/embed")
async def embed(request: EmbedRequest) -> dict[str, list[float]]:
    """
    Returns the embedding for a given text.
    """
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(None, partial(encode, [request.text]))
    return {"embedding": embedding.tolist()[0]}


@app.post("/search")
async def search(request: EmbedRequest) -> dict[str, list[dict]]:
    """
    Returns the top-1 most similar embeddings for a given text.
    """
    embedding = await embed(request)
    query = {
        "vector": embedding['embedding'],
        "topK": 1,
        "includeMetadata": True
    }
    res = requests.post("http://pinecone:5081/query", json=query)
    return {"results": res.json()}


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Returns the health status of the API.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
