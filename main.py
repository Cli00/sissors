from fastapi import FastAPI
from crud import router

app = FastAPI()

@app.get("/")
def home():
    return "Hello Server"

app.include_router(router, prefix="/users", tags=["users"])

# @router.post("/shorten/")
