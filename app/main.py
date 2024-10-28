from fastapi import FastAPI
from app.api.v1 import routes
from app.dto.resume_dto import ResumeRequest, ResumeResponse 
from app.config.settings import settings
import uvicorn

app = FastAPI()
app.include_router(routes.router)

@app.get("/")
def landing_root():
    return {"message": "Resume AI Service"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)