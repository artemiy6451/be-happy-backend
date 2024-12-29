from city.models import BuildingModel
from repository import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository):
    model = BuildingModel
