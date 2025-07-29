import io
import json
import base64
import hmac
import hashlib
from time import mktime
from datetime import datetime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from fastapi import UploadFile
import requests

# 请替换为你的讯飞开放平台凭证
APPId = "cce43f11"
APISecret = "MTkwMjFlNjgxOThiZGVkNDVmN2Y2NmVh"
APIKey = "b442a71114dfc2aa3e8eff1bddbe975b"

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

def parse_url(request_url):
    stidx = request_url.index("://")
    host = request_url[stidx + 3:]
    schema = request_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("无效的请求URL: " + request_url)
    path = host[edidx:]
    host = host[:edidx]
    return Url(host, path, schema)

def assemble_ws_auth_url(request_url, method="POST", api_key="", api_secret=""):
    """生成带认证信息的请求URL"""
    u = parse_url(request_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    
    # 构建签名原始字符串
    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"
    
    # 计算签名
    signature_sha = hmac.new(
        api_secret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature_sha = base64.b64encode(signature_sha).decode('utf-8')
    
    # 构建Authorization
    authorization_origin = (
        f"api_key=\"{api_key}\", algorithm=\"hmac-sha256\", "
        f"headers=\"host date request-line\", signature=\"{signature_sha}\""
    )
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
    
    # 拼接URL参数
    params = {
        "host": host,
        "date": date,
        "authorization": authorization
    }
    return f"{request_url}?{urlencode(params)}"

async def run_ocr(file: UploadFile) -> str:
    """
    保持与原函数相同的输入输出格式
    使用讯飞OCR接口替代pytesseract实现文字识别
    """
    # 读取文件内容
    data = await file.read()
    
    # 讯飞OCR接口地址
    url = "https://api.xf-yun.com/v1/private/sf8e6aca1"
    
    # 构建请求体
    body = {
        "header": {
            "app_id": APPId,
            "status": 3  # 表示最后一帧数据
        },
        "parameter": {
            "sf8e6aca1": {
                "category": "ch_en_public_cloud",  # 中英文通用识别
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "sf8e6aca1_data_1": {
                "encoding": file.content_type.split('/')[-1],  # 动态获取图片格式
                "image": base64.b64encode(data).decode('UTF-8'),  # 图片base64编码
                "status": 3  # 表示最后一帧数据
            }
        }
    }
    
    # 生成带认证信息的URL
    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)
    
    # 发送请求
    headers = {
        "Content-Type": "application/json",
        "host": "api.xf-yun.com"
    }
    response = requests.post(
        request_url,
        data=json.dumps(body),
        headers=headers,
        timeout=30
    )
    
    # 解析响应结果
    result = json.loads(response.text)
    # 处理API错误码
    error_codes = {
        10000: "参数错误",
        10001: "认证失败",
        10002: "权限不足",
        10003: "请求频率超限",
        10004: "服务暂不可用"
    }
    # 从header获取状态码，而非result顶层
    header_code = result.get("header", {}).get("code")
    if header_code != 0:
        error_code = header_code
        error_msg = error_codes.get(error_code, result.get("header", {}).get('message', '未知错误'))
        raise Exception(f"OCR识别失败({error_code}): {error_msg}, 完整响应: {result}")
    
    # 解码识别结果
    try:
        text_base64 = result["payload"]["result"]["text"]
        decoded_text = base64.b64decode(text_base64).decode('utf-8')
        ocr_result = json.loads(decoded_text)
        
        # 提取识别文本内容
        text_list = []
        for page in ocr_result.get('pages', []):
            for line in page.get('lines', []):
                for word in line.get('words', []):
                    text_list.append(word.get('content', ''))
        
        final_text = ' '.join(text_list).strip()
        return final_text
    except Exception as e:
        raise Exception(f"OCR结果解析失败: {str(e)}, 原始响应: {decoded_text if 'decoded_text' in locals() else '未解码'}")
