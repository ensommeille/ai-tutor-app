# backend/app/services/doubao_client.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def query_doubao(prompt: str) -> str:
    """调用豆包API获取响应"""
    api_key = os.getenv("DOUBAO_API_KEY")
    endpoint = os.getenv("DOUBAO_ENDPOINT")
    
    if not api_key or not endpoint:
        return "错误：请配置豆包API密钥和端点"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 豆包API的请求体格式（与OpenAI兼容）
    payload = {
        "model": "ernie-bot-turbo",  # 豆包免费模型，可根据实际支持的模型替换
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=30  # 超时设置
            )
            response.raise_for_status()  # 抛出HTTP错误
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    except httpx.HTTPStatusError as e:
        return f"API请求失败（状态码：{e.response.status_code}）：{await e.response.text()}"
    except KeyError as e:
        return f"API响应格式错误：缺少字段 {str(e)}"
    except Exception as e:
        return f"请求处理错误：{str(e)}"