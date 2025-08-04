import os
from dotenv import load_dotenv
import bcrypt
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone
from typing import Any


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



def get_hashed_password(password: str) -> str:
    '''
    Genera un hash seguro para una contraseña proporcionada.
    '''
    # Genera una sal aleatoria
    salt = bcrypt.gensalt()
    # Crea el hash de la contraseña utilizando la sal
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Devuelve la contraseña con el hash como una cadena de texto
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Verifica si la contraseña en texto plano coincide con el hash almacenado
    '''
    # Compara la contraseña proporcionada con el hash almacenado
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    '''
    Genera un token de acceso.
    Args:
        data(dict): Diccionario con los datos del usuario.
        expires_delta(timedelta): Tiempo de expiración del token, por default None.
    Returns:
        str: Token de acceso para el usuario.
    '''
    # Se realiza una copia de los datos del usuario
    to_encode = data.copy()
    # Se genera el tiempo de expiración (tiempo actual + tiempo expiración)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    # A la copia de los datos del usuario se agrega el tiempo de expiración
    to_encode.update({'exp': expire})
    # Devuelve el token usando los datos de usuario, llave secreta y algoritmo
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    '''
    Decodifica un token.

    Args:
        token(str): Token de acceso.

    Returns:
        dict([str, Any]): Datos del usuario decodificados a partir del token.
    '''
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except JWTError as e:
        raise Exception(f"Token inválido o expirado: {e}")