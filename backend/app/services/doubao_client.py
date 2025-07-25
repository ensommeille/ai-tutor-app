# backend/app/services/doubao_client.py
import httpx
import os
from dotenv import load_dotenv
import json
from volcenginesdkarkruntime import Ark

load_dotenv()

async def query_doubao(prompt: str, image: str = None) -> str:
    
    api_key = os.getenv("DOUBAO_API_KEY")
    client = Ark(api_key=api_key)

    # 构建消息内容
    message_content = [{
        "type": "text",
        "text": prompt
    }]
    
    # 如果有图片，添加图片内容
    if image:
        message_content.append({
            "type": "image",
            "image": image
        })

    completion = client.chat.completions.create(
        # 使用支持多模态的模型
        model="doubao-multimodal-1-6b",
        messages=[
            {"role": "user", "content": message_content}
        ]
    )
    return completion.choices[0].message.content
