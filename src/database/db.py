import os # interacción con el sistema operativo
from dotenv import load_dotenv # función para cargar de variables entorno
from motor.motor_asyncio import AsyncIOMotorClient # cliente de conexión asíncrono a mongodb 

load_dotenv() # se cargan las variables de entorno

# desde una variable de entorno se obtiene la cadena de conexión a mongo
MONGO_URI = os.getenv("MONGO_URI") 

client = AsyncIOMotorClient(MONGO_URI) # cliente de conexión a mongo
db = client.drive_and_deal_app # definición de la base de datos