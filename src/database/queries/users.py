from typing import Any # tipado de python
from src.database.db import db # base de datos en mongodb
from src.database.mongo_serializers import serialize_doc, serialize_docs


users = db.users # colección para almacenar usuarios


async def find_user(username: str) -> dict[str, Any]:
    """Función que busca por username un usuario en la base de datos.

    Args:
        username (str): nombre de usuario

    Returns:
        user (dict[str, Any]) : usuario en la base de datos
    """
    # se hace una búsqueda del usuario en la base de datos
    user = await users.find_one({"username": username})

    # si se encuentra se serializa y se retorna de lo contrario se retorna None
    return serialize_doc(user) if user else None


async def find_users() -> list[dict[str, Any]]:
    """Función para obtener todos los usuarios de la base de datos.

    Returns:
        users_list (list[dict[str, Any]]): Lista de usuarios en la base de datos
    """
    users_list = [] # se crea una lista vacía para almacenar usuarios
    cursor = users.find({}) # se hace la búsqueda en la base de datos

    # se recorre de manera asíncrona el cursor con los usuarios
    async for document in cursor:
        users_list.append(document) # se agregan los usuarios a la lista
    return serialize_docs(users_list) # se retorna la lista con las usuarios ya serializados



async def insert_user(user_data: dict[str, Any]) -> dict[str, Any]:
    """Función para insertar un usuario en la base de datos.
    
    Args:
        user_data (dict[str, Any]): Datos del usuario que se desea insertar

    Returns:
        created_user (dict[str, Any]): usuario creado
    """
    # se inserta el nuevo usuario en la base de datos
    new_user = await users.insert_one(user_data)

    # si la inserción fue éxitosa se busca la tarea
    created_user = await users.find_one({"_id": new_user.inserted_id})
    return serialize_doc(created_user) # se retorna ya serializada