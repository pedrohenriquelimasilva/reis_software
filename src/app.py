from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers import token, task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token.router)
app.include_router(task.router)