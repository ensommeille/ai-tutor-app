# backend/app/services/doubao_client.py
import httpx
import os
from dotenv import load_dotenv
import json
from volcenginesdkarkruntime import Ark

load_dotenv()

async def query_doubao(prompt: str) -> str:
    
    api_key = os.getenv("DOUBAO_API_KEY")
    client = Ark(api_key=api_key)


    completion = client.chat.completions.create(
        # 替换为模型 ID，比如"doubao-1.5-pro-32k-250115"
        model="doubao-seed-1-6-250615",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content
