from pydantic import BaseModel


class BuildingSchema(BaseModel):
    name: str
    income: int
    cost: int


class AllBuildingsSchema(BaseModel):
    buildings: list[BuildingSchema]
