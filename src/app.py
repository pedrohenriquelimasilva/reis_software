from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers import token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}