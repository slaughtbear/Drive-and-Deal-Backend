from typing import Any
from fastapi import FastAPI
from src.routes.cars import cars


app = FastAPI()


@app.get("/")
def read_root() -> dict[str, Any]:
    return {'msg': 'welcome to drive and deal backend'}


app.include_router(
    router = cars,
    prefix = "/api/cars",
    tags = ["Cars"]
)