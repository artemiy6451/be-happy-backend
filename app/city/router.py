from typing import Annotated

from city.dependencies import city_service
from city.schema import AddBuildingSchema, BuildingSchema
from city.services import CityService
from fastapi import APIRouter, Depends, status

city_router = APIRouter(prefix="/city", tags=["City"])


@city_router.post(
    "/building/add",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": BuildingSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "User already created."},
    },
)
async def add_building(
    build: AddBuildingSchema,
    service: Annotated[CityService, Depends(city_service)],
):
    building = await service.add_biulding(build)
    return building


@city_router.get(
    "/building/get_all",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_200_OK: {"model": list[BuildingSchema]},
    },
)
async def get_all_buildings(
    service: Annotated[CityService, Depends(city_service)],
):
    buildings = await service.get_all_buildings()
    return buildings
