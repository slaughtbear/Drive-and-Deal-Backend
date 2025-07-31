# Drive and Deal Backend 🚗

Backend desarrollado con **FastAPI** y **MongoDB** para un sistema de renta y reparación de autos. La aplicación gestiona múltiples roles, operaciones CRUD y autenticación segura mediante JWT.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge\&logo=python\&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge\&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge\&logo=mongodb\&logoColor=white)

---

## 📌 Descripción del Proyecto

Este backend forma parte de un sistema completo para la **gestión de renta y reparación de vehículos**, cumpliendo con los requerimientos funcionales establecidos.

Se modelaron y desarrollaron endpoints para manejar:

* Clientes
* Autos
* Rentas
* Reparaciones

Incluye seguridad con **JWT**, control de acceso por roles y consultas personalizadas.

---

## ✅ Requerimientos Funcionales Implementados

| Código   | Descripción                                                              | Actor                        |
| -------- | ------------------------------------------------------------------------ | ---------------------------- |
| **RF01** | Registro y mantenimiento de datos del cliente (alta, baja, modificación) | Empleado atención al público |
| **RF02** | Registro y mantenimiento de datos del auto                               | Encargado de autos           |
| **RF03** | Registro de reparaciones (no se eliminan)                                | Encargado de autos           |
| **RF04** | Consulta de reparaciones por periodo y monto                             | Dueño                        |
| **RF05** | Registro y actualización de renta de autos                               | Empleado atención al público |
| **RF06** | Consulta de autos más rentados en los últimos dos meses                  | Encargado de autos           |
| **RF07** | Búsqueda de autos disponibles                                            | Empleado atención al público |
| **RF08** | Alerta sobre vehículos devueltos en mal estado                           | Encargado de autos           |
| **RF09** | Registro de devoluciones de autos                                        | Encargado de autos           |

---

## 🚀 Funcionalidades Técnicas

* 🔐 Autenticación con JWT y manejo de roles (empleado, encargado, dueño)
* 🔄 CRUD para clientes, autos, rentas y reparaciones
* 📊 Consultas avanzadas por fecha, disponibilidad y estado
* 📦 Base de datos MongoDB (NoSQL)
* 📃 Documentación automática con Swagger (`/docs`)

---

## 🛠 Instalación y Configuración

Sigue estos pasos para clonar y ejecutar el proyecto localmente:

### 1. Clonar el repositorio

```bash
git clone https://github.com/slaughtbear/Drive-and-Deal-Backend.git
cd drive-and-deal-backend
```

### 2. Crear y activar un entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
MONGO_URI=mongodb://localhost:27017
FRONTEND_URL = "http://localhost:5173"
SECRET_KEY=clave_secreta_firma_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Asegúrate de tener MongoDB corriendo en tu máquina local o usar un URI de Atlas si estás usando una instancia en la nube.

### 5. Ejecutar el servidor

```bash
fastapi dev src/main.py
```

📗 Accede a la documentación automática en [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 Estructura del Proyecto

```
drive-and-deal-backend/
├── src/
│   ├── database/
│   ├── routes/
│   ├── schemas/
│   ├── __init__.py
│   └── main.py
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🧪 Endpoints principales

| Módulo                   | Endpoints                                              |
| ------------------------ | ------------------------------------------------------ |
| **Auth**                 | `/auth/login`                                          |
| **Clientes**             | `/customers/`                                            |
| **Autos**                | `/cars/`                                               |
| **Rentas**               | `/rents/`                                              |
| **Reparaciones**         | `/repairs/`                                            |

---

## 👨‍💻 Autor

Iván Aguirre – [@slaughtbear](https://github.com/slaughtbear)

---
