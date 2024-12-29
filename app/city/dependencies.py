from city.repository import CityRepository
from city.services import CityService


def city_service():
    return CityService(CityRepository)
