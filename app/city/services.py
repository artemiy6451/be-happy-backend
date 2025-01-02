from city.models import BuildingModel
from city.schema import AddBuildingSchema
from database import async_session_maker
from fastapi import HTTPException, status
from repository import AbstractRepository
from sqlalchemy.exc import IntegrityError


class CityService:
    def __init__(self, repository: type[AbstractRepository]) -> None:
        self.repository: AbstractRepository = repository(async_session_maker)

    async def add_biulding(self, bilding: AddBuildingSchema):
        try:
            building_dict = bilding.model_dump()
            building_id: int = await self.repository.add_one(building_dict)
            response: BuildingModel = await self.repository.find_one(id=building_id)
            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Can not get bilding with id: {building_id}",
                )
            bilding = response.to_read_model()
            return bilding
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Bilding already created.",
            ) from exc

    async def get_all_buildings(self):
        buildings: int = await self.repository.find_all()
        return buildings
