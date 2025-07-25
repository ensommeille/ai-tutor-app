
from openai import OpenAI
from app.config import settings

async def query_deepseek(prompt: str) -> str:
    client = OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.operatornext.cn/v1"
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return response.choices[0].message.content