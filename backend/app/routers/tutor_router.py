
from fastapi import APIRouter, UploadFile, File, Form
from app.services.ocr_service import run_ocr
from app.services.prompt_service import build_prompt
from app.services.deepseek_client import query_deepseek
from app.schemas.response import TutorResponse

router = APIRouter()

@router.post("/solve", response_model=TutorResponse)
async def solve_from_image(
    image: UploadFile = File(...),
    mode: str = Form(...),
    role: str = Form(...),
):
    text = await run_ocr(image)
    prompt = build_prompt(mode=mode, role=role, content=text)
    result = await query_deepseek(prompt)
    return TutorResponse(answer=result)
