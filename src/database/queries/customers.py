from typing import Any # tipado de python
from src.database.db import db # base de datos en mongodb
from bson import ObjectId # clase para el id de mongodb 
from src.database.mongo_serializers import serialize_doc, serialize_docs # serializadores


customers = db.customers # colección para almacenar clientes


async def find_customer(id: str) -> dict[str, Any]:
    """Función que busca por id un cliente en la base de datos.

    Args:
        id (str): ID del cliente

    Returns:
        customer (dict[str, Any]) : cliente en la base de datos
    """
    # se hace una búsqueda del cliente en la base de datos
    customer = await customers.find_one({"_id": ObjectId(id)})

    # si se encuentra se serializa y se retorna de lo contrario se retorna None
    return serialize_doc(customer) if customer else None


async def find_customers() -> list[dict[str, Any]]:
    """Función para obtener todos los clientes de la base de datos.

    Returns:
        customers_list (list[dict[str, Any]]): Lista de clientes en la base de datos
    """
    customers_list = [] # se crea una lista vacía para almacenar clientes
    cursor = customers.find({}) # se hace la búsqueda en la base de datos

    # se recorre de manera asíncrona el cursor con los clientes
    async for document in cursor:
        customers_list.append(document) # se agregan los clientes a la lista
    return serialize_docs(customers_list) # se retorna la lista con las clientes ya serializadas


async def insert_customer(customer_data: dict[str, Any]) -> dict[str, Any]:
    """Función para insertar un cliente en la base de datos.
    
    Args:
        customer_data (dict[str, Any]): Datos del cliente que se desea insertar

    Returns:
        created_customer (dict[str, Any]): cliente creado
    """
    # se inserta la nueva tarea en la base de datos
    new_customer = await customers.insert_one(customer_data)

    # si la inserción fue éxitosa se busca la tarea
    created_customer = await customers.find_one({"_id": new_customer.inserted_id})
    return serialize_doc(created_customer) # se retorna ya serializada


async def update_one_customer(id: str, customer_data: dict[str, Any]) -> dict[str, Any]:
    """Función para actualizar una tarea en la base de datos.

    Args:
        id (str): ID de la tarea que se desea actualizar
        customer_data (dict[str, Any])): Datos de la tarea que se desea actualizar

    Returns:
        updated_task (dict[str, Any]): Tarea actualizada
    """
    # se obtienen sólo los datos proporcionados para actualizar el cliente
    customer = {k: v for k, v in customer_data.items() if v is not None}

    # se actualiza el cliente en la base de datos con la información dada
    result = await customers.update_one({"_id": ObjectId(id)}, {"$set": customer})
    if result.matched_count == 0: # si no se logra la actualización
        return None # se retorna None
    
    # si la actualización fue éxitosa se busca el cliente actualizado
    updated_customer = await customers.find_one({"_id": ObjectId(id)})
    return serialize_doc(updated_customer) # se retorna ya serializado


async def delete_one_customer(id: str) -> bool:
    """Función para eliminar un cliente en la base de datos.

    Args:
        id (str): ID del cliente que se desea eliminar

    Returns
        bool: True si la eliminación fue éxitosa
    """
    # se realiza la eliminación del cliente de la base de datos    
    result = await customers.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1 # si se elimina el cliente se retorna True de lo contrario False