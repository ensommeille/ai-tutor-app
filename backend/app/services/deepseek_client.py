
import httpx
from app.config import settings

async def query_deepseek(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"}
    async with httpx.AsyncClient() as client:
        r = await client.post(settings.DEEPSEEK_ENDPOINT, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"]
