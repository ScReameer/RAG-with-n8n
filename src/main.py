import uvicorn
import requests
import asyncio
import os
from functools import partial
from fastapi import FastAPI
from pydantic import BaseModel
from encoder import encode, load_model
import httpx


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
N8N_WEBHOOK_URL_PROD = os.getenv('N8N_WEBHOOK_URL_PROD', '')
N8N_WEBHOOK_URL_TEST = os.getenv('N8N_WEBHOOK_URL_TEST', '')
last_update_id = 0

load_model()

app = FastAPI()


class EmbedRequest(BaseModel):
    """
    Request model for embedding
    """
    text: str


@app.post("/embed")
async def embed(request: EmbedRequest):
    """
    Returns the embedding for a given text.
    """
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(None, partial(encode, [request.text]))
    return {"embedding": embedding.tolist()[0]}


@app.post("/search")
async def search(request: EmbedRequest):
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

async def poll_telegram():
    global last_update_id

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(
                    f"{TELEGRAM_API_URL}/getUpdates",
                    params={"offset": last_update_id + 1, "timeout": 30}
                )
                updates = response.json()

                if updates.get("ok"):
                    for update in updates["result"]:
                        last_update_id = update["update_id"]

                        if "message" in update and "text" in update["message"]:
                            await client.post(N8N_WEBHOOK_URL_TEST, json=update)
                            await client.post(N8N_WEBHOOK_URL_PROD, json=update)

            except httpx.ReadTimeout:
                pass

            except Exception as e:
                print(f"[poll_telegram] Unexpected error: {repr(e)}")

            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(poll_telegram())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
