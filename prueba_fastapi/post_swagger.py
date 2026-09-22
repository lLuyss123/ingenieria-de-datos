from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Modelo que representa los datos que el cliente
# debe enviar para crear un producto.
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    categoria: str
    stock: int
    descripcion: str | None = None


# Modelo que representa lo que nuestro servidor
# devolverá después de crear el producto.
#
# El cliente no envía id ni creado_en.
# Estos campos los genera nuestro servidor.
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    categoria: str
    stock: int
    descripcion: str | None
    creado_en: datetime


# Lista que utilizaremos como almacenamiento temporal.
# Los productos desaparecen cuando se reinicia el servidor.
productos = []


# Variable para generar los IDs.
# Comenzamos desde 1.
siguiente_id = 1


@app.get("/productos")
def get_productos():
    # Devuelve todos los productos almacenados.
    return productos


@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=201
)
def create_producto(producto: ProductoCreate):

    global siguiente_id

    # Validamos una regla de negocio:
    # el precio debe ser mayor que cero.
    if producto.precio <= 0:
        raise HTTPException(
            status_code=400,
            detail="El precio debe ser mayor a cero"
        )

    # Validamos otra regla de negocio:
    # el stock no puede ser negativo.
    if producto.stock < 0:
        raise HTTPException(
            status_code=400,
            detail="El stock no puede ser negativo"
        )

    # Creamos el producto completo.
    producto_creado = ProductoResponse(
        id=siguiente_id,
        nombre=producto.nombre,
        precio=producto.precio,
        categoria=producto.categoria,
        stock=producto.stock,
        descripcion=producto.descripcion,
        creado_en=datetime.now(timezone.utc)
    )

    # Guardamos el producto en nuestra lista.
    productos.append(producto_creado)

    # Aumentamos el ID para el siguiente producto.
    siguiente_id += 1

    return producto_creado