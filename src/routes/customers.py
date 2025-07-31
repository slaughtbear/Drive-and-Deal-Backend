from fastapi import APIRouter, HTTPException
from bson.errors import InvalidId
from src.schemas.customers import Customer, CustomerCreate, CustomerUpdate
from src.database.queries.customers import (
    find_customers,
    find_customer,
    insert_customer,
    update_one_customer,
    delete_one_customer
)

""" RF01
    El sistema debe permitir al Empleado de atención al público, registrar y mantener los datos del cliente.
"""

customers = APIRouter()


@customers.get("/", response_model=list[Customer])
async def get_all_customers() -> list[Customer]:
    """Endpoint de tipo GET para obtener una lista de clientes.

    Returns:
        customers_list (list[Car]): Lista de clientes.
    """
    customers_list = await find_customers()
    return customers_list


@customers.get("/{id}", response_model=Customer)
async def get_customer(id: str) -> Customer:
    """Endpoint de tipo GET para obtener un cliente por ID.

    Args:
        id (str): ID del cliente que se desea obtener.

    Returns:
        car (Car): Cliente buscado.
    """
    try:
        stored_customer = await find_customer(id)
        if not stored_customer:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return stored_customer
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@customers.post("/", response_model=Customer)
async def create_customer(customer_data: CustomerCreate) -> Customer:
    """Endpoint de tipo POST para registrar un cliente.

    Args:
        customer_data (CustomerCreate): Datos del cliente que se desea registrar.

    Returns:
        response (Customer): Cliente creado.
    """
    response = await insert_customer(customer_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500, # internal server error
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response


@customers.put("/{id}", response_model=Customer)
async def update_customer(id: str, customer_data: CustomerUpdate) -> Customer:
    """Endpoint de tipo PUT para actualizar un cliente.

    Args:
        id (str): ID del cliente que se desea actualizar.
    """
    try:
        response = await update_one_customer(id, customer_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@customers.delete("/{id}")
async def delete_customer(id: str) -> dict[str, str]:
    """Endpoint de tipo GET para eliminar un cliente por ID.

    Args:
        id (str): ID del cliente que se desea eliminar.

    Returns:
        dict[str, str]: Mensaje de respuesta al eliminar el cliente.
    """
    try:
        response = await delete_one_customer(id)
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado el cliente con el ID {id} en la base de datos."
            )
        return {"msg": "Cliente eliminado correctamente."}
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )