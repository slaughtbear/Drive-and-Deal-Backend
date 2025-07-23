from fastapi import APIRouter, HTTPException
from src.database.queries.rentals import delete_one_rental, find_rental, find_rentals, insert_rental, update_one_rental
from src.schemas.rentals import Rental, RentalCreate, RentalUpdate
from bson.errors import InvalidId # excepción cuando un ID no es compatible con el de mongodb


rentals = APIRouter()


@rentals.get("/", response_model=list[Rental])
async def get_all_rentals() -> list[Rental]:
    """Endpoint de tipo GET para obtener una lista de rentas.

    Returns:
        rentals_list (list[Rental]): Lista de rentas.
    """
    rentals_list = await find_rentals()
    return rentals_list


@rentals.get("/{id}", response_model=Rental)
async def get_rental(id: str) -> Rental:
    """Endpoint de tipo GET para obtener una renta por ID.

    Args:
        id (str): ID de la renta que se desea obtener.

    Returns:
        rental (Rental): Renta buscada.
    """
    try:
        stored_rental = await find_rental(id)
        if not stored_rental:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
            )
        return stored_rental
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@rentals.post("/", response_model=Rental)
async def create_rental(rental_data: RentalCreate) -> Rental:
    """Endpoint de tipo POST para registrar una rentas.

    Args:
        rental_data (RentalCreate): Datos de la renta que se desea registrar.

    Returns:
        response (Rental): Renta creada.
    """
    response = await insert_rental(rental_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500, # internal server error
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response


@rentals.put("/{id}", response_model=Rental)
async def update_rental(id: str, rental_data: RentalUpdate) -> Rental:
    """Endpoint de tipo PUT para actualizar una renta.

    Args:
        id (str): ID de la renta que se desea actualizar.
    """
    try:
        response = await update_one_rental(id, rental_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@rentals.delete("/{id}")
async def delete_rental(id: str) -> dict[str, str]:
    """Endpoint de tipo GET para eliminar una renta por ID.

    Args:
        id (str): ID de la renta que se desea eliminar.

    Returns:
        dict[str, str]: Mensaje de respuesta al eliminar la renta.
    """
    try:
        response = await delete_one_rental(id)
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
            )
        return {"msg": "renta eliminada correctamente."}
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )