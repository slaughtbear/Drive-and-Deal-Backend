from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    '''Clase base de usuario para enviar datos al frontend.'''
    id: str
    username: str
    full_name:str
    role: str
    disabled: bool


class UserInDB(User):
    '''Clase para mostrar todos los datos almacenados en MongoDB del usuario.'''
    hashed_password: str


class UserCreate(BaseModel):
    '''Clase para validar la creación de un usuario.'''
    username: str = Field(min_length=6, max_length=24)
    # TODO: Mejorar validación contraseñas
    password: str = Field(min_length=8)
    password_confirm: str
    full_name: str = Field(min_length=6, max_length=24)
    # TODO: Añadir validación de roles
    role: str


class UserUpdate(BaseModel):
    '''Clase para validar la actualización de un usuario.'''
    username: Optional[str] = Field(min_length=6, max_length=24)
    # TODO: Mejorar validación contraseñas
    password: Optional[str] = Field(min_length=8)
    password_confirm: str
    full_name: Optional[str] = Field(min_length=6, max_length=24)
    # TODO: Añadir validación de roles
    role: Optional[str]