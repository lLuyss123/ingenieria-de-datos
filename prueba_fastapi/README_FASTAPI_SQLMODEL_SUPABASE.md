# FastAPI CRUD con SQLModel y PostgreSQL

API REST sencilla desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL (Supabase)**.

El objetivo del proyecto es entender cómo pasar de una API que trabaja solamente con datos en memoria a una API que puede **guardar y consultar información de una base de datos**.

La estructura se mantiene sencilla y separada por responsabilidades para que cada archivo tenga una función clara.

---

## 1. Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI** — creación de la API y sus endpoints.
- **SQLModel** — definición de los modelos y comunicación con la base de datos.
- **PostgreSQL** — base de datos.
- **Supabase** — servicio utilizado para alojar PostgreSQL.
- **uv** — gestión del proyecto, dependencias y ejecución.
- **python-dotenv** — lectura de variables de entorno desde `.env`.
- **psycopg** — driver que permite a Python conectarse con PostgreSQL.

---

## 2. Estructura del proyecto

```text
prueba_fastapi/
│
├── main.py
├── models.py
├── database.py
├── .env
├── .gitignore
├── pyproject.toml
└── uv.lock
```

Cada archivo tiene una responsabilidad específica:

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Define la API y sus endpoints |
| `models.py` | Define los modelos de datos |
| `database.py` | Configura la conexión con PostgreSQL |
| `.env` | Guarda la URL de conexión de forma privada |
| `.gitignore` | Evita subir archivos o información que no deben estar en Git |
| `pyproject.toml` | Define el proyecto y sus dependencias |
| `uv.lock` | Registra las versiones exactas de las dependencias |

---

# 3. ¿Cómo se construyó el proyecto?

El proyecto se construyó siguiendo un orden lógico.

```text
1. Crear proyecto con uv
        ↓
2. Instalar dependencias
        ↓
3. Crear base de datos en Supabase
        ↓
4. Guardar la conexión en .env
        ↓
5. Crear database.py
        ↓
6. Crear models.py
        ↓
7. Crear main.py
        ↓
8. Crear la tabla si no existe
        ↓
9. Crear endpoints
        ↓
10. Probar la API con Swagger
```

La razón de seguir este orden es que cada paso depende del anterior.

Primero necesitamos el proyecto y sus herramientas, después la conexión, luego los modelos y finalmente los endpoints que utilizan todo lo anterior.

---

# 4. Creación del proyecto con uv

El proyecto utiliza **uv** para administrar Python y las dependencias.

Por ejemplo:

```bash
uv init
```

Después se agregaron las dependencias necesarias:

```bash
uv add fastapi sqlmodel python-dotenv "psycopg[binary]"
```

### ¿Por qué uv?

Porque permite administrar las dependencias del proyecto desde `pyproject.toml` y mantener un archivo `uv.lock` con las versiones utilizadas.

Esto permite que el proyecto pueda reproducirse de una manera más consistente.

---

# 5. Configuración de PostgreSQL con Supabase

La aplicación necesita una base de datos donde guardar los productos.

Para este proyecto se utilizó PostgreSQL mediante Supabase.

La conexión no se escribe directamente en `main.py` ni en `models.py`.

En su lugar, se guarda en:

```text
.env
```

Ejemplo:

```env
DATABASE_URL="postgresql+psycopg://usuario:contraseña@host:5432/postgres"
```

La contraseña real no debe escribirse directamente en el código ni subirse a GitHub.

---

# 6. database.py

El archivo `database.py` se encarga únicamente de preparar la conexión con PostgreSQL.

```python
import os

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

engine = create_engine(DATABASE_URL)
```

## ¿Qué ocurre aquí?

### 1. Cargar variables de entorno

```python
load_dotenv()
```

Busca el archivo `.env` y carga sus variables.

---

### 2. Obtener la URL de la base de datos

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

Busca la variable:

```text
DATABASE_URL
```

que está definida en `.env`.

---

### 3. Comprobar que exista

```python
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")
```

Si la URL no existe, la aplicación se detiene mostrando un error claro.

Esto evita intentar conectarse a una base de datos sin tener una dirección de conexión.

---

### 4. Crear el engine

```python
engine = create_engine(DATABASE_URL)
```

El `engine` representa la configuración que SQLModel utilizará para comunicarse con PostgreSQL.

Por eso `database.py` se puede entender como:

```text
.env
 ↓
DATABASE_URL
 ↓
create_engine()
 ↓
engine
```

---

# 7. models.py

El archivo `models.py` contiene los modelos relacionados con los productos.

```python
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int


class ProductCreate(SQLModel):
    name: str
    price: float
    stock: int
```

---

## 7.1 Product

```python
class Product(SQLModel, table=True):
```

El parámetro:

```python
table=True
```

indica que `Product` representa una tabla de la base de datos.

El modelo contiene:

```text
id
name
price
stock
```

### ID

```python
id: int | None = Field(default=None, primary_key=True)
```

El `id` es la clave primaria.

Es opcional al momento de crear el objeto porque normalmente la base de datos se encarga de generar su valor.

---

## 7.2 ProductCreate

```python
class ProductCreate(SQLModel):
```

Este modelo representa los datos que esperamos recibir cuando alguien quiere crear un producto.

No contiene `id` porque el usuario no necesita enviarlo.

Por ejemplo:

```json
{
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
```

La diferencia principal es:

```text
Product
   ↓
Representa el producto almacenado en la base de datos

ProductCreate
   ↓
Representa los datos necesarios para crear un producto
```

---

# 8. main.py

`main.py` es el archivo que contiene la API y sus endpoints.

```python
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, SQLModel, select

from database import engine
from models import Product, ProductCreate

app = FastAPI()


SQLModel.metadata.create_all(engine)


@app.get("/products")
def get_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product


@app.post("/products")
def create_product(product: ProductCreate):
    with Session(engine) as session:
        new_product = Product(**product.model_dump())

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product
```

---

# 9. Orden de funcionamiento de main.py

El flujo principal es:

```text
database.py
     ↓
   engine
     ↓
main.py
     ↓
SQLModel.metadata.create_all()
     ↓
Session
     ↓
select / add
     ↓
PostgreSQL
```

Ahora se puede entender cada parte.

---

## 9.1 Crear la aplicación

```python
app = FastAPI()
```

Crea la aplicación FastAPI.

A partir de este objeto se registran los endpoints.

---

## 9.2 Crear las tablas

```python
SQLModel.metadata.create_all(engine)
```

SQLModel utiliza los modelos que tienen:

```python
table=True
```

para conocer qué tablas necesita.

En este caso conoce:

```python
Product
```

y utiliza el `engine` para comprobar la base de datos.

Si la tabla no existe, la crea.

Si ya existe, no la vuelve a crear.

Por eso este proyecto no necesita Alembic para este flujo básico.

---

# 10. GET /products

```python
@app.get("/products")
def get_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products
```

Este endpoint obtiene todos los productos.

El flujo es:

```text
GET /products
      ↓
crear Session
      ↓
select(Product)
      ↓
consultar PostgreSQL
      ↓
.all()
      ↓
devolver productos
```

### `Session`

```python
with Session(engine) as session:
```

La `Session` representa la interacción con la base de datos durante esa operación.

---

### `select(Product)`

```python
select(Product)
```

Indica que queremos consultar los registros de `Product`.

---

### `.all()`

```python
.all()
```

Obtiene todos los resultados.

---

# 11. GET /products/{product_id}

```python
@app.get("/products/{product_id}")
def get_product(product_id: int):
```

Este endpoint busca un producto específico mediante su ID.

Por ejemplo:

```text
GET /products/1
```

El valor:

```text
1
```

se recibe en:

```python
product_id
```

Después se crea la consulta:

```python
statement = select(Product).where(Product.id == product_id)
```

Esto significa:

```text
Busca en Product
donde Product.id
sea igual al ID recibido
```

Luego:

```python
product = session.exec(statement).first()
```

obtiene el primer resultado.

Si no existe:

```python
if not product:
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
```

la API responde:

```text
404 Not Found
```

---

# 12. POST /products

```python
@app.post("/products")
def create_product(product: ProductCreate):
```

Este endpoint recibe los datos de un nuevo producto.

Ejemplo:

```json
{
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
```

FastAPI valida esos datos utilizando `ProductCreate`.

---

## 12.1 Convertir los datos

```python
new_product = Product(**product.model_dump())
```

`model_dump()` convierte el modelo en un diccionario.

Conceptualmente:

```text
ProductCreate
      ↓
model_dump()
      ↓
{
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
      ↓
Product
```

El `**` permite pasar esos valores al constructor de `Product`.

---

## 12.2 Agregar el producto

```python
session.add(new_product)
```

Prepara el nuevo producto para ser guardado.

---

## 12.3 Confirmar el cambio

```python
session.commit()
```

Confirma la operación en PostgreSQL.

Este es el momento en que el cambio queda guardado en la base de datos.

---

## 12.4 Actualizar el objeto

```python
session.refresh(new_product)
```

Actualiza el objeto con la información que pueda haber generado la base de datos, como el `id`.

Por ejemplo, antes del `commit`:

```text
name = "Manzana"
price = 1251
stock = 4
id = None
```

Después de guardar:

```text
id = 1
name = "Manzana"
price = 1251
stock = 4
```

---

# 13. Flujo completo de creación de un producto

Cuando hacemos:

```text
POST /products
```

ocurre:

```text
Usuario
   ↓
JSON
   ↓
FastAPI
   ↓
ProductCreate
   ↓
Product
   ↓
Session
   ↓
session.add()
   ↓
session.commit()
   ↓
PostgreSQL
   ↓
session.refresh()
   ↓
Respuesta de la API
```

---

# 14. Flujo completo de consulta

Cuando hacemos:

```text
GET /products
```

ocurre:

```text
Usuario
   ↓
GET /products
   ↓
FastAPI
   ↓
Session
   ↓
select(Product)
   ↓
PostgreSQL
   ↓
Resultados
   ↓
FastAPI
   ↓
JSON
```

---

# 15. ¿Por qué separamos los archivos?

Aunque el proyecto es pequeño, separar responsabilidades hace que sea más fácil entenderlo y mantenerlo.

```text
models.py
    ↓
¿Qué datos maneja la aplicación?

database.py
    ↓
¿Cómo se conecta a la base de datos?

main.py
    ↓
¿Qué puede hacer la API?
```

Así evitamos colocar toda la lógica en un solo archivo.

---

# 16. ¿Por qué no usamos Alembic?

En este proyecto se decidió mantener una implementación sencilla.

Para este nivel del proyecto se utiliza:

```python
SQLModel.metadata.create_all(engine)
```

Esto permite crear las tablas que no existan.

Alembic es una herramienta útil para manejar migraciones y cambios de estructura de una base de datos en proyectos más grandes, pero no es necesaria para entender primero el flujo básico:

```text
FastAPI
   ↓
SQLModel
   ↓
Session
   ↓
PostgreSQL
```

Por eso se dejó fuera de esta implementación.

---

# 17. Ejecución del proyecto

Como el proyecto utiliza `uv`, la aplicación se ejecuta con:

```bash
uv run fastapi dev main.py
```

Después se puede abrir la documentación interactiva de FastAPI:

```text
/docs
```

Por ejemplo:

```text
http://127.0.0.1:8000/docs
```

---

# 18. Endpoints disponibles

| Método | Endpoint | Función |
|---|---|---|
| GET | `/products` | Obtener todos los productos |
| GET | `/products/{product_id}` | Obtener un producto por ID |
| POST | `/products` | Crear un producto |

---

# 19. Ejemplo de uso

### Crear producto

```http
POST /products
```

Body:

```json
{
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
```

Respuesta:

```json
{
    "id": 1,
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
```

### Consultar productos

```http
GET /products
```

Respuesta:

```json
[
    {
        "id": 1,
        "name": "Manzana",
        "price": 1251,
        "stock": 4
    }
]
```

### Consultar un producto

```http
GET /products/1
```

Respuesta:

```json
{
    "id": 1,
    "name": "Manzana",
    "price": 1251,
    "stock": 4
}
```

---

# 20. Resumen conceptual

El proyecto completo se puede recordar con este flujo:

```text
                  FASTAPI
                     │
                     ▼
                  main.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      models.py             database.py
          │                     │
          │                     ▼
          │                   engine
          │                     │
          └──────────┬──────────┘
                     ▼
                  Session
                     │
                     ▼
                PostgreSQL
                  Supabase
```

La idea fundamental es:

> **`models.py` define los datos, `database.py` prepara la conexión y `main.py` utiliza ambos para construir la API.**

Ese es el flujo básico que se construyó en este proyecto.
