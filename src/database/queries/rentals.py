from datetime import datetime, timezone
from typing import Any # tipado de python
from src.database.db import db # base de datos en mongodb
from bson import ObjectId # clase para el id de mongodb 
from src.database.mongo_serializers import serialize_doc, serialize_docs # serializadores


rentals = db.rentals # colección para almacenar rentas


async def find_rental(id: str) -> dict[str, Any]:
    """Función que busca por id una renta en la base de datos.

    Args:
        id (str): ID del renta

    Returns:
        rental (dict[str, Any]) : renta en la base de datos
    """
    # se hace una búsqueda del renta en la base de datos
    rental = await rentals.find_one({"_id": ObjectId(id)})
    
    if rental:
        rental["id_customer"] = str(rental["id_customer"])
        rental["id_car"] = str(rental["id_car"])
        return serialize_doc(rental)

    # si se encuentra se serializa y se retorna de lo contrario se retorna None
    return None


async def find_rentals() -> list[dict[str, Any]]:
    """Función para obtener todos los rentas de la base de datos.

    Returns:
        rentals_list (list[dict[str, Any]]): Lista de rentas en la base de datos
    """
    rentals_list = [] # se crea una lista vacía para almacenar rentas
    cursor = rentals.find({}) # se hace la búsqueda en la base de datos

    # se recorre de manera asíncrona el cursor con los rentas
    async for document in cursor:
        document["id_customer"] = str(document["id_customer"])
        document["id_car"] = str(document["id_car"])
        rentals_list.append(document) # se agregan los rentas a la lista
    return serialize_docs(rentals_list) # se retorna la lista con las rentas ya serializadas


async def insert_rental(rental_data: dict[str, Any]) -> dict[str, Any]:
    """Función para insertar una renta de renta en la base de datos.
    
    Args:
        rental_data (dict[str, Any]): Datos del renta que se desea insertar

    Returns:
        created_rental (dict[str, Any]): renta creado
    """
    # se establece la fecha de inicio de la renta en formato y horario UTC
    rental_data["start_date"] = datetime.now(timezone.utc)

    rental_data["id_customer"] = ObjectId(rental_data["id_customer"])
    rental_data["id_car"] = ObjectId(rental_data["id_car"])

    # se inserta la nueva renta en la base de datos
    new_rental = await rentals.insert_one(rental_data)

    # si la inserción fue éxitosa se busca la renta
    created_rental = await rentals.find_one({"_id": new_rental.inserted_id})
    created_rental["id_customer"] = str(created_rental["id_customer"])
    created_rental["id_car"] = str(created_rental["id_car"])
    return serialize_doc(created_rental) # se retorna ya serializada


async def update_one_rental(id: str, rental_data: dict[str, Any]) -> dict[str, Any]:
    """Función para actualizar una renta en la base de datos.

    Args:
        id (str): ID de la renta que se desea actualizar
        rental_data (dict[str, Any])): Datos de la renta que se desea actualizar

    Returns:
        updated_task (dict[str, Any]): renta actualizada
    """
    # se obtienen sólo los datos proporcionados para actualizar el renta
    rental = {k: v for k, v in rental_data.items() if v is not None}

    # se actualiza el renta en la base de datos con la información dada
    result = await rentals.update_one({"_id": ObjectId(id)}, {"$set": rental})
    if result.matched_count == 0: # si no se logra la actualización
        return None # se retorna None
    
    # si la actualización fue éxitosa se busca el renta actualizado
    updated_rental = await rentals.find_one({"_id": ObjectId(id)})
    updated_rental["id_customer"] = str(updated_rental["id_customer"])
    updated_rental["id_car"] = str(updated_rental["id_car"])
    return serialize_doc(updated_rental) # se retorna ya serializado


async def delete_one_rental(id: str) -> bool:
    """Función para eliminar una renta de renta en la base de datos.

    Args:
        id (str): ID del renta que se desea eliminar

    Returns
        bool: True si la eliminación fue éxitosa
    """
    # se realiza la eliminación del renta de la base de datos    
    result = await rentals.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1 # si se elimina el renta se retorna True de lo contrario False