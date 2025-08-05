from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from bson.errors import InvalidId 
from src.schemas.repairs import Repair, RepairCreate, RepairUpdate
from src.database.queries.repairs import (
    find_repairs,
    find_repair,
    find_repairs_by_filters,
    insert_repair,
    update_one_repair
)
from src.security.dependencies import check_manager_or_owner, check_manager, check_owner

repairs = APIRouter()

# RF03: Accesible por managers y dueños
@repairs.get("/", response_model=list[Repair])
async def get_all_repairs(user = Depends(check_manager_or_owner)) -> list[Repair]:
    repairs_list = await find_repairs()
    return repairs_list

# RF03: Accesible por managers y dueños
@repairs.get("/{id}", response_model=Repair)
async def get_repair(id: str, user = Depends(check_manager_or_owner)) -> Repair:
    try:
        stored_repair = await find_repair(id)
        if not stored_repair:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado la reparación con el ID {id} en la base de datos."
            )
        return stored_repair
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )
    
# RF04: Solo dueño
@repairs.get("/filter/", response_model=list[Repair])
async def filter_repairs(
    registered_at: date | None = None, 
    mount: float | None = None,
    user = Depends(check_owner)
) -> list[Repair]:
    repairs_list = await find_repairs_by_filters(registered_at, mount)
    return repairs_list

# RF03: Solo manager
@repairs.post("/", response_model=Repair)
async def create_repair(repair_data: RepairCreate, user = Depends(check_manager)) -> Repair:
    response = await insert_repair(repair_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500,
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response

# RF03: Solo manager
@repairs.put("/{id}", response_model=Repair)
async def update_repair(id: str, repair_data: RepairUpdate, user = Depends(check_manager)) -> Repair:
    try:
        response = await update_one_repair(id, repair_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado la reparación con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )