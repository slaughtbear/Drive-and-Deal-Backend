from pydantic import BaseModel, Field, EmailStr


class Customer(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone_number: str
    address: str


class CustomerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, example="Juan Pérez")
    email: EmailStr = Field(example="juan.perez@email.com")
    phone_number: str = Field(min_length=7, max_length=15, example="5551234567")
    address: str = Field(min_length=5, max_length=100, example="Calle Falsa 123, Ciudad")


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=7, max_length=15)
    address: str | None = Field(default=None, min_length=5, max_length=100)