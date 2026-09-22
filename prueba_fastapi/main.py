from fastapi import FastAPI, HTTPException
# Importamos dos cosas de FastAPI:
#
# FastAPI → nos permite crear nuestra aplicación y sus endpoints.
#
# HTTPException → nos permite devolver errores HTTP personalizados,
# por ejemplo un error 404 cuando un producto no existe.


from sqlmodel import Session, SQLModel, select
# Importamos tres cosas de SQLModel:
#
# Session → permite trabajar con la base de datos.
#
# SQLModel → lo usamos para crear las tablas a partir de nuestros modelos.
#
# select → nos permite construir consultas para buscar información
# en la base de datos.



from database import engine
# Importamos el engine que creamos en database.py.
#
# Ese engine contiene la configuración necesaria para comunicarnos
# con nuestra base de datos PostgreSQL.


from models import Product, ProductCreate
# Importamos nuestros dos modelos desde models.py.
#
# Product → representa el producto que está en la base de datos.
#
# ProductCreate → representa los datos que recibimos cuando
# queremos crear un producto.


app = FastAPI()
# Creamos nuestra aplicación FastAPI.
#
# A partir de "app" vamos a definir nuestros endpoints:
#
# GET /products
# GET /products/{id}
# POST /products


# Crear las tablas si no existen
SQLModel.metadata.create_all(engine)
# Le decimos a SQLModel que cree las tablas correspondientes
# a nuestros modelos que tengan table=True.
#
# En nuestro caso:
#
# Product
#    ↓
# tabla product
#
# "engine" le indica en qué base de datos debe hacerlo.
#
# Si la tabla no existe → la crea.
# Si la tabla ya existe → no la vuelve a crear.

@app.get("/products")
# Creamos un endpoint GET para:
#
# GET /products
#
# Cuando alguien haga una petición a esta dirección,
# se ejecutará la función que está debajo.


def get_products():
    # Esta función se ejecuta cuando hacemos GET /products.

    with Session(engine) as session:
        # Creamos una Session para trabajar con PostgreSQL.
        #
        # "engine" indica qué conexión/base de datos utilizaremos.
        #
        # "session" será nuestro medio para hacer operaciones
        # contra la base de datos.
        #
        # "with" hace que la sesión se cierre correctamente
        # cuando terminemos de trabajar con ella.

        products = session.exec(select(Product)).all()
        # Aquí hacemos la consulta.
        #
        # select(Product)
        # significa:
        # "Quiero consultar los registros de Product".
        #
        # session.exec(...)
        # ejecuta esa consulta en la base de datos.
        #
        # .all()
        # obtiene todos los resultados.
        #
        # Finalmente guardamos esos resultados en "products".

        return products
        # Devolvemos los productos.
        #
        # FastAPI convierte automáticamente los objetos
        # en una respuesta JSON.


@app.get("/products/{id}")
# Creamos otro endpoint GET.
#
# La parte:
#
# {id}
#
# significa que el ID viene directamente en la URL.
#
# Ejemplo:
#
# GET /products/5
#
# En ese caso id será 5.


def get_product(id: int):
    # Recibimos el ID como un entero.
    #
    # Si hacemos:
    #
    # /products/5
    #
    # entonces:
    #
    # id = 5


    with Session(engine) as session:
        # Abrimos una sesión para consultar PostgreSQL.


        statement = select(Product).where(Product.id == id)
        # Construimos nuestra consulta.
        #
        # select(Product)
        # → queremos buscar productos.
        #
        # .where(...)
        # → ponemos una condición.
        #
        # Product.id == id
        # → buscamos el producto cuyo ID sea igual
        # al ID que recibimos en la URL.
        #
        # Por ejemplo:
        #
        # GET /products/5
        #
        # sería conceptualmente:
        #
        # buscar Product donde id = 5


        product = session.exec(statement).first()
        # Ejecutamos la consulta.
        #
        # .first()
        # obtiene el primer resultado.
        #
        # Si encontramos el producto:
        #
        # product = ese producto
        #
        # Si no existe:
        #
        # product = None


        if not product:
            # Comprobamos si no encontramos ningún producto.

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
            # Si no existe, devolvemos un error HTTP 404.
            #
            # 404 significa:
            # "No encontrado".
            #
            # detail contiene el mensaje que verá el usuario.


        return product
        # Si encontramos el producto,
        # lo devolvemos como respuesta.

@app.post("/products")
# Creamos un endpoint POST.
#
# POST normalmente se utiliza cuando queremos
# crear información nueva.


def create_product(product: ProductCreate):
    # Recibimos los datos enviados por el usuario.
    #
    # FastAPI utiliza ProductCreate para validar
    # que los datos tengan la estructura esperada.
    #
    # Por ejemplo:
    #
    # {
    #     "name": "Manzana",
    #     "price": 1251,
    #     "stock": 4
    # }


    with Session(engine) as session:
        # Abrimos una sesión con PostgreSQL.


        new_product = Product(**product.model_dump())
        # Aquí convertimos ProductCreate en Product.
        #
        # product.model_dump()
        # convierte el objeto en un diccionario.
        #
        # Conceptualmente:
        #
        # {
        #     "name": "Manzana",
        #     "price": 1251,
        #     "stock": 4
        # }
        #
        # El ** permite pasar esos datos al modelo Product.
        #
        # Finalmente obtenemos:
        #
        # new_product = Product(...)


        session.add(new_product)
        # Agregamos el nuevo producto a la sesión.
        #
        # Todavía no significa que ya esté guardado
        # definitivamente en PostgreSQL.
        #
        # Simplemente estamos preparando la operación.


        session.commit()
        # Confirmamos la operación.
        #
        # Aquí se guarda definitivamente el nuevo producto
        # en PostgreSQL.


        session.refresh(new_product)
        # Actualizamos el objeto después de guardarlo.
        #
        # Esto es especialmente importante para obtener
        # valores generados por la base de datos,
        # como el ID.


        return new_product
        # Devolvemos el producto creado.

@app.put("/products/{id}")
def update_product(id: int, product: ProductCreate):
    # Recibimos el ID del producto que queremos actualizar
    # y los nuevos datos del producto.

    with Session(engine) as session:
        # Abrimos una sesión con la base de datos.

        statement = select(Product).where(Product.id == id)
        # Buscamos el producto que queremos actualizar
        # utilizando el ID recibido en la URL.

        existing_product = session.exec(statement).first()
        # Ejecutamos la consulta y obtenemos el producto.
        #
        # Si existe → obtenemos el producto.
        # Si no existe → obtenemos None.

        if not existing_product:
            # Comprobamos si el producto no existe.

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
            # Si no existe, devolvemos un error 404.


        existing_product.name = product.name
        existing_product.price = product.price
        existing_product.stock = product.stock
        existing_product.category = product.category
        existing_product.description = product.description
        # Actualizamos los datos del producto existente
        # con los nuevos datos que recibimos.


        session.add(existing_product)
        # Le indicamos a la sesión que estamos trabajando
        # con este producto actualizado.

        session.commit()
        # Guardamos los cambios definitivamente
        # en PostgreSQL.

        session.refresh(existing_product)
        # Actualizamos el objeto con los datos que quedaron
        # finalmente en la base de datos.

        return existing_product
        # Devolvemos el producto actualizado.

@app.delete("/products/{id}")
def delete_product(id: int):
    # Recibimos el ID del producto que queremos eliminar.

    with Session(engine) as session:
        # Abrimos una sesión con la base de datos.

        statement = select(Product).where(Product.id == id)
        # Buscamos el producto utilizando el ID recibido.

        product = session.exec(statement).first()
        # Ejecutamos la consulta y obtenemos el producto.
        #
        # Si existe → obtenemos el producto.
        # Si no existe → obtenemos None.

        if not product:
            # Comprobamos si el producto no existe.

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
            # Si no existe, devolvemos un error 404.


        session.delete(product)
        # Marcamos el producto para eliminarlo
        # de la base de datos.


        session.commit()
        # Confirmamos la eliminación en PostgreSQL.


        return {"message": "Product deleted successfully"}
        # Devolvemos un mensaje indicando que
        # el producto fue eliminado correctamente.