from city.schema import BuildingSchema
from models import Base
from sqlalchemy.orm import Mapped, mapped_column


class BuildingModel(Base):
    __tablename__ = "buildings"
    name: Mapped[str] = mapped_column(unique=True)
    income: Mapped[int]
    cost: Mapped[int]

    def to_read_model(self):
        return BuildingSchema(
            name=self.name,
            income=self.income,
            cost=self.cost,
        )
