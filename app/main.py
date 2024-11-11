from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes
from app.dto.resume_dto import ResumeRequest, ResumeResponse 
from app.config.settings import settings
import uvicorn

app = FastAPI()
app.include_router(routes.router)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처를 허용. 보안이 필요하면 특정 출처를 설정하세요.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def landing_root():
    print(settings.host)
    print(settings.port)
    return {"message": "Resume AI Service"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

# uvicorn app.main:app --reload