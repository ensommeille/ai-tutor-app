
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tutor_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(tutor_router.router, prefix="/api/tutor", tags=["Tutor"])
