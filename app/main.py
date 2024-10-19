from fastapi import FastAPI
from app.api.v1 import routes

app = FastAPI()

app.include_router(routes.router)

#testing
@app.get("/")
def read_root():
    return {"message": "Resume AI Service"}
    