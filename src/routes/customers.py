from fastapi import APIRouter, HTTPException, Depends
from bson.errors import InvalidId
from src.schemas.customers import Customer, CustomerCreate, CustomerUpdate
from src.database.queries.customers import (
    find_customers,
    find_customer,
    insert_customer,
    update_one_customer,
    delete_one_customer
)
from src.security.dependencies import check_employee

customers = APIRouter()

# RF01: Solo empleado
@customers.get("/", response_model=list[Customer])
async def get_all_customers(user = Depends(check_employee)) -> list[Customer]:
    customers_list = await find_customers()
    return customers_list

# RF01: Solo empleado
@customers.get("/{id}", response_model=Customer)
async def get_customer(id: str, user = Depends(check_employee)) -> Customer:
    try:
        stored_customer = await find_customer(id)
        if not stored_customer:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return stored_customer
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )

# RF01: Solo empleado
@customers.post("/", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, user = Depends(check_employee)) -> Customer:
    response = await insert_customer(customer_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500,
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response

# RF01: Solo empleado
@customers.put("/{id}", response_model=Customer)
async def update_customer(id: str, customer_data: CustomerUpdate, user = Depends(check_employee)) -> Customer:
    try:
        response = await update_one_customer(id, customer_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )

# RF01: Solo empleado
@customers.delete("/{id}")
async def delete_customer(id: str, user = Depends(check_employee)) -> dict[str, str]:
    try:
        response = await delete_one_customer(id)
        if not response:
            raise HTTPException(
                status_code = 404,
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return {"msg": "Cliente eliminado correctamente."}
    except InvalidId:
        raise HTTPException(
            status_code = 400,
            detail = "El ID proporcionado no es válido."
        )