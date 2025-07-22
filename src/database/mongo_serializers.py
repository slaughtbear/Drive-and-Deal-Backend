from typing import Any # tipado de python

def serialize_doc(doc: dict[str, Any]) -> dict[str, Any]:
    """Serializador que convierte el ObjectId de un documento a str y lo mapea al atributo id.

    Args:
        doc (dict[str, Any]): Diccionario con los datos del documento a serializar

    Returns:
        doc (dict[str, Any]): Documento serializado con el id como str
    """
    # se crea una llave "id" en el diccionario y toma el valor de la llave "_id"
    doc["id"] = str(doc["_id"])
    del doc["_id"] # elimina la llave "_id"
    return doc # se retorna el documento con formato compatible con los esquemas pydantic

def serialize_docs(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Serializador que convierte el ObjectId a str y lo mapea al atributo id en una lista de documentos.

    Args:
        docs (list[dict[str, Any]]): Lista de documentos a serializar

    Returns:
        docs (list[dict[str, Any]]): Lista de documentos serializados con el id como str

    Returns
    """
    # se retorna una lista de documentos serializados
    return [serialize_doc(doc) for doc in docs]