import os # interacción con el sistema operativo
from dotenv import load_dotenv # función para cargar de variables entorno
from motor.motor_asyncio import AsyncIOMotorClient # cliente de conexión asíncrono a mongodb 

load_dotenv() # se cargan las variables de entorno

# desde una variable de entorno se obtiene la cadena de conexión a mongo
MONGO_URI = os.getenv("MONGO_URI") 

client = AsyncIOMotorClient(MONGO_URI) # cliente de conexión a mongo
db = client.drive_and_deal_app # definición de la base de datos

# PRUEBA DE CONEXIÓN
# Ejecuta en la terminal: python -m src.database.db
async def test_connection() -> None:
    try:
        result = await client.admin.command('ping')
        print("Conexión exitosa:", result)
    except Exception as e:
        print("Error de conexión:", e)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())