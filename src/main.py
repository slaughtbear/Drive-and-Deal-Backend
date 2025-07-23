from typing import Any
from fastapi import FastAPI
from src.routes.cars import cars
from src.routes.customers import customers
from src.routes.rentals import rentals
from src.routes.repairs import repairs


app = FastAPI(title="Drive and Deal Backend")


@app.get("/")
def read_root() -> dict[str, Any]:
    return {'msg': 'welcome to drive and deal backend'}


app.include_router(
    router = cars,
    prefix = "/api/cars",
    tags = ["Autos"]
)

app.include_router(
    router = customers,
    prefix = "/api/customers",
    tags = ["Clientes"]
)

app.include_router(
    router = rentals,
    prefix = "/api/rentals",
    tags = ["Rentas"]
)


app.include_router(
    router = repairs,
    prefix = "/api/repairs",
    tags = ["Reparaciones"]
)