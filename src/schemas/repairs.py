from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class Repair(BaseModel):
    id: str
    id_car: str
    description: str
    mount: float
    registered_at: date


class RepairCreate(BaseModel):
    id_car: str = Field(min_length=1, example="66a1c...")
    description: str = Field(min_length=5, max_length=100, example="Cambio de aceite y filtro")
    mount: float = Field(ge=0, example=500.0)


class RepairUpdate(BaseModel):
    description: Optional[str] = Field(default=None, min_length=5, max_length=100)
    mount: Optional[float] = Field(default=None, ge=0)