from fastapi import APIRouter, HTTPException
from src.database.queries.cars import delete_one_car, find_car, find_cars, insert_car, update_one_car
from src.schemas.cars import Car, CarCreate, CarUpdate
from bson.errors import InvalidId # excepción cuando un ID no es compatible con el de mongodb


cars = APIRouter()


@cars.get("/", response_model=list[Car])
async def get_all_cars() -> list[Car]:
    """Endpoint de tipo GET para obtener una lista de autos.

    Returns:
        cars_list (list[Car]): Lista de autos.
    """
    cars_list = await find_cars()
    return cars_list


@cars.get("/{id}", response_model=Car)
async def get_car(id: str) -> Car:
    """Endpoint de tipo GET para obtener un auto por ID.

    Args:
        id (str): ID del auto que se desea obtener.

    Returns:
        car (Car): Auto buscado.
    """
    try:
        stored_car = await find_car(id)
        if not stored_car:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return stored_car
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@cars.post("/", response_model=Car)
async def create_car(car_data: CarCreate) -> Car:
    """Endpoint de tipo POST para registrar un auto.

    Args:
        car_data (CarCreate): Datos del auto que se desea registrar.

    Returns:
        response (Car): Auto creada.
    """
    response = await insert_car(car_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500, # internal server error
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response


@cars.put("/{id}", response_model=Car)
async def update_car(id: str, car_data: CarUpdate) -> Car:
    """Endpoint de tipo PUT para actualizar un auto.

    Args:
        id (str): ID del auto que se desea actualizar.
    """
    try:
        response = await update_one_car(id, car_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@cars.delete("/{id}")
async def delete_car(id: str) -> dict[str, str]:
    """Endpoint de tipo GET para eliminar un auto por ID.

    Args:
        id (str): ID del auto que se desea eliminar.

    Returns:
        dict[str, str]: Mensaje de respuesta al eliminar el auto.
    """
    try:
        response = await delete_one_car(id)
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el auto con el ID {id} en la base de datos."
            )
        return {"msg": "Auto eliminada correctamente."}
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )