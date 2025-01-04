from city.schema import BuildingSchema
from models import Base
from sqlalchemy.orm import Mapped, mapped_column


class BuildingModel(Base):
    __tablename__ = "buildings"
    name: Mapped[str] = mapped_column(unique=True)
    income: Mapped[int]
    cost: Mapped[int]
    icon_url: Mapped[str]

    def to_read_model(self):
        return BuildingSchema(
            id=self.id,
            name=self.name,
            income=self.income,
            cost=self.cost,
            icon_url=self.icon_url,
        )
