
from openai import AsyncOpenAI
from app.config import settings

async def query_deepseek(prompt: str):
    client = AsyncOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.operatornext.cn/v1"
    )
    stream = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        stream=True
    )
    async for chunk in stream:
        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            yield content