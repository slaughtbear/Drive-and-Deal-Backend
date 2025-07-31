from datetime import date
from typing import Any # tipado de python
from src.database.db import db # base de datos en mongodb
from bson import ObjectId # clase para el id de mongodb 
from src.database.mongo_serializers import serialize_doc, serialize_docs # serializadores


repairs = db.repairs # colección para almacenar reparaciones


async def find_repair(id: str) -> dict[str, Any]:
    """Función que busca por id una reparación en la base de datos.

    Args:
        id (str): ID del reparación

    Returns:
        repair (dict[str, Any]) : reparación en la base de datos
    """
    # se hace una búsqueda del reparación en la base de datos
    repair = await repairs.find_one({"_id": ObjectId(id)})
    
    if repair: # si se encuentra se serializa y se retorna de lo contrario se retorna None
        repair["id_car"] = str(repair["id_car"])
        return serialize_doc(repair)

    return None


async def find_repairs() -> list[dict[str, Any]]:
    """Función para obtener todos los reparaciones de la base de datos.

    Returns:
        repairs_list (list[dict[str, Any]]): Lista de reparaciones en la base de datos
    """
    repairs_list = [] # se crea una lista vacía para almacenar reparaciones
    cursor = repairs.find({}) # se hace la búsqueda en la base de datos

    # se recorre de manera asíncrona el cursor con los reparaciones
    async for document in cursor:
        document["id_car"] = str(document["id_car"])
        repairs_list.append(document) # se agregan los reparaciones a la lista
    return serialize_docs(repairs_list) # se retorna la lista con las reparaciones ya serializadas


async def find_repairs_by_filters(
    date_filter: date | None = None, 
    mount_filter: float | None = None
) -> list[dict[str, Any]]:
    """Función para obtener reparaciones filtradas por fecha y/o monto.
    
    Args:
        date_filter (date | None): Fecha de registro para filtrar (opcional)
        mount_filter (float | None): Monto para filtrar (opcional)
        
    Returns:
        list[dict[str, Any]]: Lista de reparaciones que coinciden con los filtros
    """
    query = {} # diccionario para almacenar queries
    
    if date_filter is not None: # si se proporciona una fecha
        query["registered_at"] = date_filter.isoformat()
    
    if mount_filter is not None: # si se proporciona un monto
        query["mount"] = mount_filter
    
    repairs_list = [] # lista para almacenar las reparaciones
    cursor = repairs.find(query) # se ejecuta el query a la base de datos
    
    async for document in cursor: # se recorre el cursor con los documentos filtrados
        # se serializa el ID del carro para devolverlo en formato str
        document["id_car"] = str(document["id_car"]) 
        repairs_list.append(document) # se agrega el documento a la lista
    return serialize_docs(repairs_list) # se serializa la lista de documentos su ID a str


async def insert_repair(repair_data: dict[str, Any]) -> dict[str, Any]:
    """Función para insertar una reparación de reparación en la base de datos.
    
    Args:
        repair_data (dict[str, Any]): Datos del reparación que se desea insertar

    Returns:
        created_repair (dict[str, Any]): reparación creado
    """
    # se establece la fecha de inicio de la renta en formato y horario UTC
    repair_data["registered_at"] = date.today().isoformat()
    repair_data["id_car"] = ObjectId(repair_data["id_car"])

    # se inserta la nueva reparación en la base de datos
    new_repair = await repairs.insert_one(repair_data)

    # si la inserción fue éxitosa se busca la reparación
    created_repair = await repairs.find_one({"_id": new_repair.inserted_id})
    created_repair["id_car"] = str(created_repair["id_car"])
    return serialize_doc(created_repair) # se retorna ya serializada


async def update_one_repair(id: str, repair_data: dict[str, Any]) -> dict[str, Any]:
    """Función para actualizar una reparación en la base de datos.

    Args:
        id (str): ID de la reparación que se desea actualizar
        repair_data (dict[str, Any])): Datos de la reparación que se desea actualizar

    Returns:
        updated_task (dict[str, Any]): reparación actualizada
    """
    # se obtienen sólo los datos proporcionados para actualizar el reparación
    repair = {k: v for k, v in repair_data.items() if v is not None}

    # se actualiza el reparación en la base de datos con la información dada
    result = await repairs.update_one({"_id": ObjectId(id)}, {"$set": repair})
    if result.matched_count == 0: # si no se logra la actualización
        return None # se retorna None
    
    # si la actualización fue éxitosa se busca el reparación actualizado
    updated_repair = await repairs.find_one({"_id": ObjectId(id)})
    updated_repair["id_car"] = str(updated_repair["id_car"])
    return serialize_doc(updated_repair) # se retorna ya serializado


async def delete_one_repair(id: str) -> bool:
    """Función para eliminar una reparación de reparación en la base de datos.

    Args:
        id (str): ID del reparación que se desea eliminar

    Returns
        bool: True si la eliminación fue éxitosa
    """
    # se realiza la eliminación del reparación de la base de datos    
    result = await repairs.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1 # si se elimina el reparación se retorna True de lo contrario False