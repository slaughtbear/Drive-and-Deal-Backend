from datetime import datetime
from pydantic import BaseModel, Field


class Repair(BaseModel):
    id: str
    id_car: str
    description: str
    mount: float
    date: datetime


class RepairCreate(BaseModel):
    id_car: str = Field(min_length=1, example="66a1c...")
    description: str = Field(min_length=5, max_length=100, example="Cambio de aceite y filtro")
    mount: float = Field(ge=0, example=500.0)


class RepairUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=5, max_length=100)
    mount: float | None = Field(default=None, ge=0)
    date: datetime | None = None