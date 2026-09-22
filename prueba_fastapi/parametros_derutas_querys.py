from fastapi import FastAPI, HTTPException, Query

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
    # Endpoint para comprobar que la API está funcionando.
    return {"status": "ok"}


@app.get("/")
def get_store_info():
    # Devuelve información general de la tienda.
    return {
        "nombre": "Tech Store",
        "version": "1.0.0",
        "total_productos": len(productos)
    }


@app.get("/productos")
def get_products(
    # default = valor que se utiliza si el usuario
    # no proporciona el parámetro.
    #
    # ge = greater than or equal (mayor o igual que).
    # skip debe ser mayor o igual a 0.
    skip: int = Query(
        default=0,
        ge=0,
        description="Cantidad de productos a omitir"
    ),

    # default = si no se proporciona limit, será 10.
    #
    # ge = el valor mínimo permitido es 1.
    #
    # le = less than or equal (menor o igual que).
    # El valor máximo permitido es 50.
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Cantidad máxima de productos"
    ),

    # Parámetro opcional para filtrar por categoría.
    # Si no se proporciona, su valor será None.
    categoria: str | None = None,

    # Parámetro opcional para buscar por nombre.
    # Si no se proporciona, su valor será None.
    busqueda: str | None = None
):

    # Comenzamos con todos los productos.
    productos_filtrados = productos


    # Si el usuario proporcionó una categoría,
    # filtramos los productos.
    if categoria:

        productos_filtrados = []

        for producto in productos:

            # lower() convierte el texto a minúsculas para
            # que no importe si el usuario escribe:
            # "Electrónica", "electrónica" o "ELECTRÓNICA".
            if producto["categoria"].lower() == categoria.lower():

                # Agregamos a la nueva lista únicamente
                # los productos que coinciden con la categoría.
                productos_filtrados.append(producto)


    # Si el usuario proporcionó una búsqueda,
    # filtramos por el nombre del producto.
    if busqueda:

        productos_filtrados_busqueda = []

        for producto in productos_filtrados:

            # "in" comprueba si el texto buscado aparece
            # dentro del nombre del producto.
            #
            # Por ejemplo:
            # "teclado" in "teclado mecánico" → True
            if busqueda.lower() in producto["nombre"].lower():

                productos_filtrados_busqueda.append(producto)

        productos_filtrados = productos_filtrados_busqueda


    # Aplicamos la paginación después de realizar los filtros.
    #
    # skip indica desde qué posición empezamos.
    # limit indica cuántos productos queremos devolver.
    return productos_filtrados[skip:skip + limit]


@app.get("/productos/{id}")
def get_product(id: int):

    # Recorremos todos los productos buscando
    # el producto cuyo ID coincida con el recibido.
    for producto in productos:

        if producto["id"] == id:
            return producto


    # Si terminamos el for y no encontramos el producto,
    # devolvemos un error HTTP 404.
    raise HTTPException(
        status_code=404,
        detail=f"Producto con id {id} no encontrado"
    )