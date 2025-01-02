from city.router import city_router
from config import Settings
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.router import user_router

app = FastAPI()

origins = ["https://localhost", "https://localhost:5173", Settings().cors_ip]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers: list[APIRouter] = [user_router, city_router]

for router in routers:
    app.include_router(router)
