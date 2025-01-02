from pydantic import BaseModel


class AddBuildingSchema(BaseModel):
    name: str
    income: int
    cost: int


class BuildingSchema(AddBuildingSchema):
    id: int


class AllBuildingsSchema(BaseModel):
    buildings: list[BuildingSchema]
