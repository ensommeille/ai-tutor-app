
from fastapi import APIRouter, UploadFile, File, Form
import base64
from app.services.ocr_service import run_ocr
from app.services.prompt_service import build_prompt
from app.services.doubao_client import query_doubao
from app.schemas.response import TutorResponse

router = APIRouter()

@router.post("/solve", response_model=TutorResponse)
async def solve_from_image(
    image: UploadFile = File(...),
    mode: str = Form(...),
    role: str = Form(...),
):
    # 读取图片并转换为base64
    image_data = await image.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    # 构建文本提示词
    prompt_text = build_prompt(mode=mode, role=role, content="请分析以下图片中的数学题并解答:")
    
    # 将图片和文本分别传递给模型
    result = await query_doubao(prompt=prompt_text, image=base64_image)
    return TutorResponse(answer=result)
