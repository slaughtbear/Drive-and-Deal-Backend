from datetime import date, timedelta
from collections import Counter
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.rentals import Rental, RentalCreate, RentalUpdate
from src.database.queries.rentals import (
    find_rentals,
    find_rental,
    insert_rental,
    update_one_rental
)
from src.security.dependencies import check_employee

rentals = APIRouter()

# RF05: Accesible por empleados y managers
@rentals.get("/", response_model=list[Rental])
async def get_all_rentals(
    filter_rental: bool = None,
    user = Depends(check_employee)
) -> list[Rental]:
    rentals_list = await find_rentals()

    if filter_rental:
        two_months_ago = date.today() - timedelta(days=60)
        recent_rentals = [
            rental for rental in rentals_list
            if rental["start_date"] >= two_months_ago
        ]
        car_ids = [rental["id_car"] for rental in recent_rentals]
        car_count = Counter(car_ids)
        most_rented = car_count.most_common()
        return most_rented
    
    return rentals_list

# RF05: Accesible por empleados y managers
@rentals.get("/{id}", response_model=Rental)
async def get_rental(id: str, user = Depends(check_employee)) -> Rental:
    try:
        stored_rental = await find_rental(id)
        if not stored_rental:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
            )
        return stored_rental
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )

# RF05: Solo empleado
@rentals.post("/", response_model=Rental)
async def create_rental(rental_data: RentalCreate, user = Depends(check_employee)) -> Rental:
    response = await insert_rental(rental_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500,
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response

# RF05: Solo empleado
@rentals.put("/{id}", response_model=Rental)
async def update_rental(id: str, rental_data: RentalUpdate, user = Depends(check_employee)) -> Rental:
    try:
        response = await update_one_rental(id, rental_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado la renta con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )