from fastapi import FastAPI

app = FastAPI()


productos = [
    {
        "id": 1,
        "nombre": "Laptop",
        "precio": 2500000,
        "categoria": "Electrónica",
        "stock": 10
    },
    {
        "id": 2,
        "nombre": "Mouse",
        "precio": 80000,
        "categoria": "Accesorios",
        "stock": 25
    },
    {
        "id": 3,
        "nombre": "Teclado",
        "precio": 150000,
        "categoria": "Accesorios",
        "stock": 15
    },
    {
        "id": 4,
        "nombre": "Monitor",
        "precio": 900000,
        "categoria": "Electrónica",
        "stock": 8
    },
    {
        "id": 5,
        "nombre": "Audífonos",
        "precio": 200000,
        "categoria": "Audio",
        "stock": 20
    }
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def get_store_info():
    return {
        "nombre": "Tech Store",
        "version": "1.0.0",
        "total_productos": len(productos)
    }


@app.get("/productos")
def get_products():
    return productos