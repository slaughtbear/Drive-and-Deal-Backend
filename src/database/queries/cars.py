from typing import Any # tipado de python
from src.database.db import db # base de datos en mongodb
from bson import ObjectId # clase para el id de mongodb 
from src.database.mongo_serializers import serialize_doc, serialize_docs # serializadores


cars = db.cars # colección para almacenar tareas


async def find_car(id: str) -> dict[str, Any]:
    """Función que busca por id un auto en la base de datos.

    Args:
        id (str): ID del auto

    Returns:
        car (dict[str, Any]) : auto en la base de datos
    """
    # se hace una búsqueda del auto en la base de datos
    car = await cars.find_one({"_id": ObjectId(id)})

    # si se encuentra se serializa y se retorna de lo contrario se retorna None
    return serialize_doc(car) if car else None


async def find_cars() -> list[dict[str, Any]]:
    """Función para obtener todos los autos de la base de datos.

    Returns:
        cars_list (list[dict[str, Any]]): Lista de autos en la base de datos
    """
    cars_list = [] # se crea una lista vacía para almacenar autos
    cursor = cars.find({}) # se hace la búsqueda en la base de datos

    # se recorre de manera asíncrona el cursor con los autos
    async for document in cursor:
        cars_list.append(document) # se agregan los autos a la lista
    return serialize_docs(cars_list) # se retorna la lista con las autos ya serializadas


async def insert_car(car_data: dict[str, Any]) -> dict[str, Any]:
    """Función para insertar un auto en la base de datos.
    
    Args:
        car_data (dict[str, Any]): Datos del auto que se desea insertar

    Returns:
        created_car (dict[str, Any]): Auto creado
    """
    # se inserta la nueva tarea en la base de datos
    new_car = await cars.insert_one(car_data)

    # si la inserción fue éxitosa se busca la tarea
    created_car = await cars.find_one({"_id": new_car.inserted_id})
    return serialize_doc(created_car) # se retorna ya serializada


async def update_one_car(id: str, car_data: dict[str, Any]) -> dict[str, Any]:
    """Función para actualizar una tarea en la base de datos.

    Args:
        id (str): ID de la tarea que se desea actualizar
        car_data (dict[str, Any])): Datos de la tarea que se desea actualizar

    Returns:
        updated_task (dict[str, Any]): Tarea actualizada
    """
    # se obtienen sólo los datos proporcionados para actualizar el auto
    car = {k: v for k, v in car_data.items() if v is not None}

    # se actualiza el auto en la base de datos con la información dada
    result = await cars.update_one({"_id": ObjectId(id)}, {"$set": car})
    if result.matched_count == 0: # si no se logra la actualización
        return None # se retorna None
    
    # si la actualización fue éxitosa se busca el auto actualizado
    updated_car = await cars.find_one({"_id": ObjectId(id)})
    return serialize_doc(updated_car) # se retorna ya serializado


async def delete_one_car(id: str) -> bool:
    """Función para eliminar un auto en la base de datos.

    Args:
        id (str): ID del auto que se desea eliminar

    Returns
        bool: True si la eliminación fue éxitosa
    """
    # se realiza la eliminación del auto de la base de datos    
    result = await cars.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1 # si se elimina el auto se retorna True de lo contrario False