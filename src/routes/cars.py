from fastapi import APIRouter, HTTPException, Depends
from bson.errors import InvalidId
from src.schemas.cars import Car, CarCreate, CarUpdate
from src.database.queries.cars import (
    find_cars,
    find_car,
    find_cars_by_filters,
    insert_car,
    update_one_car,
    delete_one_car
)
from src.security.dependencies import check_manager, check_employee, check_employee_or_manager

cars = APIRouter()

# RF07: Accesible por empleados y managers
@cars.get("/", response_model=list[Car])
async def get_all_cars(user = Depends(check_employee_or_manager)) -> list[Car]:
    cars_list = await find_cars()
    return cars_list

@cars.get("/{id}", response_model=Car)
async def get_car(id: str, user = Depends(check_employee_or_manager)) -> Car:
    try:
        stored_car = await find_car(id)
        if not stored_car:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return stored_car
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )
    
# RF07: Accesible por empleados y managers
@cars.get("/filter/", response_model=list[Car])
async def filter_cars(
    avaible: bool | None = None,
    user = Depends(check_employee)
) -> list[Car]:
    cars_list = await find_cars_by_filters(avaible)
    return cars_list

# RF02: Solo manager
@cars.post("/", response_model=Car)
async def create_car(car_data: CarCreate, user = Depends(check_manager)) -> Car:
    response = await insert_car(car_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500,
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response

# RF02: Solo manager
@cars.put("/{id}", response_model=Car)
async def update_car(id: str, car_data: CarUpdate, user = Depends(check_manager)) -> Car:
    try:
        response = await update_one_car(id, car_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )

# RF02: Solo manager
@cars.delete("/{id}")
async def delete_car(id: str, user = Depends(check_manager)) -> dict[str, str]:
    try:
        response = await delete_one_car(id)
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return {"msg": "Auto eliminado correctamente."}
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )