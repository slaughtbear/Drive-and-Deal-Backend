import os
from typing import Any
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.cars import cars
from src.routes.customers import customers
from src.routes.rentals import rentals
from src.routes.repairs import repairs


app = FastAPI(title="Drive and Deal Backend")


load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [FRONTEND_URL],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


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