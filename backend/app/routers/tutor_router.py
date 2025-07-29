
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.services.ocr_service import run_ocr
from app.services.prompt_service import build_prompt
from app.services.doubao_client import query_doubao
from app.services.deepseek_client import query_deepseek


router = APIRouter()

@router.post("/solve")
async def solve_from_image(
    image: UploadFile = File(...),
    mode: str = Form(...),
    role: str = Form(...),
):
    text = await run_ocr(image)
    print(text)
    prompt = build_prompt(mode=mode, role=role, content=text)
    print(prompt)
    async def stream_generator():
        async for chunk in query_deepseek(prompt):
            yield chunk.encode("utf-8")
    return StreamingResponse(stream_generator(), media_type="text/plain")
