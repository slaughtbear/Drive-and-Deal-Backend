from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Rental(BaseModel):
    id: str
    id_customer: str
    id_car: str
    start_date: datetime
    end_date: datetime = None
    total_amount: float
    returned: bool = False
    return_status: str = None


class RentalCreate(BaseModel):
    id_customer: str = Field(min_length=1, example="66a1b...")
    id_car: str = Field(min_length=1, example="66a1c...")
    total_amount: float = Field(ge=0, example=1500.0)


class RentalUpdate(BaseModel):
    end_date: Optional[datetime] = None
    total_amount: Optional[float] = Field(default=None, ge=0)
    returned: Optional[bool] = None
    return_status: Optional[str] = Field(default=None, min_length=3, max_length=30)