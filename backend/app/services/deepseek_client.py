
import httpx
from app.config import settings

async def query_deepseek(prompt: str) -> str:
    payload = {
        "model": "deepseek-chat",  # 替换为 DeepSeek 支持的模型名称
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"  # 补充必要的 Content-Type 头
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(settings.DEEPSEEK_ENDPOINT, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"]
