from pydantic import BaseModel, Field


class Car(BaseModel):
    id: str
    brand: str
    model: str
    year: int
    license_plate: str
    avaible: bool
    state: str


class CarCreate(BaseModel):
    brand: str = Field(
        min_length=3,
        max_length=32,
        example="Nissan"
    )
    model: str = Field(
        min_length=3,
        max_length=32,
        example="Skyline GT-R (R35)"
    )
    year: int = Field(
        ge=1900,
        le=2025,
        example=2007
    )
    license_plate: str = Field(
        min_length=5,
        max_length=12,
        example="ABC1234"
    )
    avaible: bool = Field(
        example=True
    )
    state: str = Field(
        min_length=3,
        max_length=20,
        example="Disponible"
    )


class CarUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=3, max_length=32)
    model: str | None = Field(default=None, min_length=1, max_length=32)
    year: int | None = Field(default=None, ge=1886, le=2100)
    license_plate: str | None = Field(default=None, min_length=5, max_length=12)
    avaible: bool | None = None
    state: str | None = Field(default=None, min_length=3, max_length=20)