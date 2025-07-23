from fastapi import APIRouter, HTTPException
from src.database.queries.repairs import find_repair, find_repairs, insert_repair, update_one_repair
from src.schemas.repairs import Repair, RepairCreate, RepairUpdate
from bson.errors import InvalidId # excepción cuando un ID no es compatible con el de mongodb


repairs = APIRouter()


@repairs.get("/", response_model=list[Repair])
async def get_all_repairs() -> list[Repair]:
    """Endpoint de tipo GET para obtener una lista de reparaciones.

    Returns:
        repairs_list (list[Repair]): Lista de reparaciones.
    """
    repairs_list = await find_repairs()
    return repairs_list


@repairs.get("/{id}", response_model=Repair)
async def get_repair(id: str) -> Repair:
    """Endpoint de tipo GET para obtener una reparación por ID.

    Args:
        id (str): ID de la reparación que se desea obtener.

    Returns:
        repair (Repair): Reparación buscada.
    """
    try:
        stored_repair = await find_repair(id)
        if not stored_repair:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado la reparación con el ID {id} en la base de datos."
            )
        return stored_repair
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


@repairs.post("/", response_model=Repair)
async def create_repair(repair_data: RepairCreate) -> Repair:
    """Endpoint de tipo POST para registrar una reparaciones.

    Args:
        repair_data (RepairCreate): Datos de la reparación que se desea registrar.

    Returns:
        response (repair): Reparación creada.
    """
    response = await insert_repair(repair_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500, # internal server error
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response


@repairs.put("/{id}", response_model=Repair)
async def update_repair(id: str, repair_data: RepairUpdate) -> Repair:
    """Endpoint de tipo PUT para actualizar una reparación.

    Args:
        id (str): ID de la reparación que se desea actualizar.
    """
    try:
        response = await update_one_repair(id, repair_data.model_dump())
        if not response:
            raise HTTPException(
                status_code = 404, # not found
                detail = f"No se ha encontrado la reparación con el ID {id} en la base de datos."
            )
        return response
    except InvalidId:
        raise HTTPException(
            status_code = 400, # bad request
            detail = "El ID proporcionado no es válido."
        )


# @repairs.delete("/{id}")
# async def delete_repair(id: str) -> dict[str, str]:
#     """Endpoint de tipo GET para eliminar una reparación por ID.

#     Args:
#         id (str): ID de la reparación que se desea eliminar.

#     Returns:
#         dict[str, str]: Mensaje de respuesta al eliminar la reparación.
#     """
#     try:
#         response = await delete_one_repair(id)
#         if not response:
#             raise HTTPException(
#                 status_code = 404, # not found
#                 detail = f"No se ha encontrado la reparación con el ID {id} en la base de datos."
#             )
#         return {"msg": "reparación eliminada correctamente."}
#     except InvalidId:
#         raise HTTPException(
#             status_code = 400, # bad request
#             detail = "El ID proporcionado no es válido."
#         )