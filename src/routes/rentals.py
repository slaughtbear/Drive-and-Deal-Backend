from datetime import date, timedelta
from collections import Counter
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException
from src.schemas.rentals import Rental, RentalCreate, RentalUpdate
from src.database.queries.rentals import (
    find_rentals,
    find_rental,
    insert_rental,
    update_one_rental,
    # delete_one_rental
)

""" RF05
    El sistema debe permitir registrar y actualizar la renta de un auto.
"""

rentals = APIRouter()

""" RF06
    El sistema debe permitir consultar autos más rentados en los últimos dos meses.
"""
@rentals.get("/", response_model=list[Rental])
async def get_all_rentals(filter_rental: bool = None) -> list[Rental]:
    """Endpoint de tipo GET para obtener una lista de rentas.

    Returns:
        rentals_list (list[Rental]): Lista de rentas.
    """
    rentals_list = await find_rentals()

    if filter_rental:
        two_months_ago = date.today() - timedelta(days=60)

        # Filtrar rentas en los últimos 2 meses
        recent_rentals = [
            rental for rental in rentals_list
            if rental["start_date"] >= two_months_ago
        ]
        
        # Contar cuántas veces se rentó cada auto
        car_ids = [rental["id_car"] for rental in recent_rentals]
        car_count = Counter(car_ids)
        
        # Ordenar por cantidad de rentas (mayor a menor)
        most_rented = car_count.most_common()
        
        return most_rented  # Lista de tuplas: (id_car, cantidad)
    
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


# @rentals.delete("/{id}")
# async def delete_rental(id: str) -> dict[str, str]:
#     """Endpoint de tipo GET para eliminar una renta por ID.

#     Args:
#         id (str): ID de la renta que se desea eliminar.

#     Returns:
#         dict[str, str]: Mensaje de respuesta al eliminar la renta.
#     """
#     try:
#         response = await delete_one_rental(id)
#         if not response:
#             raise HTTPException(
#                 status_code = 404, # not found
#                 detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
#             )
#         return {"msg": "renta eliminada correctamente."}
#     except InvalidId:
#         raise HTTPException(
#             status_code = 400, # bad request
#             detail = "El ID proporcionado no es válido."
#         )