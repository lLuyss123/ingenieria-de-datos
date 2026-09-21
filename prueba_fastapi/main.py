from fastapi import FastAPI,Query
from pydantic import BaseModel

class Producto(BaseModel):
    id: str
    nombre: str
    precio: float
    quantity: int
    categoria: str  


app = FastAPI()
productos = [ 
    {
        "id": "ROPA-001",
        "nombre": "Camiseta Básica de Algodón",
        "precio": 15.99,
        "quantity": 50,
        "categoria": "Ropa y Moda"
    },
    {
        "id": "ROPA-002",
        "nombre": "Pantalón Jeans Clásico",
        "precio": 39.99,
        "quantity": 30,
        "categoria": "Ropa y Moda"
    },
    {
        "id": "TEC-001",
        "nombre": "Audífonos Inalámbricos",
        "precio": 29.99,
        "quantity": 25,
        "categoria": "Tecnología"
    },
    {
        "id": "TEC-002",
        "nombre": "Reloj Inteligente (Smartwatch)",
        "precio": 59.99,
        "quantity": 15,
        "categoria": "Tecnología"
    },
    {
        "id": "HOG-001",
        "nombre": "Botella Térmica de Acero",
        "precio": 18.50,
        "quantity": 40,
        "categoria": "Hogar y Varios"
    },
    {
        "id": "HOG-002",
        "nombre": "Lámpara de Escritorio LED",
        "precio": 24.99,
        "quantity": 20,
        "categoria": "Hogar y Varios"
    }
]




@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Productos",
            "Nombre": "La esquina JHN",
            "version": "1.0.0",
            "Total productos": len(productos)}
    

@app.get("/productos")
def get_productos(
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=10, ge=1, le=50, description="Máximo de registros a retornar"),
    
    
):
    
    productos_filtrados = productos[skip: skip + limit]
    
    productos_total = len(productos)
    
    return {
        "metadata": {
            "total_productos": productos_total,
            "skip": skip,
            "limit": limit
        },
        "data": productos_filtrados
    }
    


@app.get("/productos/{id}")
def get_productos_by_id(id: str):
    for producto in productos:
        
        if producto["id"]== id:
            return producto
        
        else:
            return {"message": "Producto no encontrado"}