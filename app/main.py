from city.router import city_router
from fastapi import APIRouter, FastAPI
from user.router import user_router

app = FastAPI()

routers: list[APIRouter] = [user_router, city_router]

for router in routers:
    app.include_router(router)
