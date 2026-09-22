import os
# Importamos el módulo os de Python.
# Lo vamos a utilizar para poder leer variables de entorno,
# como nuestra DATABASE_URL.


from dotenv import load_dotenv
# Importamos load_dotenv.
# Esta función permite cargar las variables que tenemos
# guardadas dentro del archivo .env.


from sqlmodel import create_engine
# Importamos create_engine de SQLModel.
# create_engine nos permite crear la conexión/configuración
# que utilizaremos para comunicarnos con PostgreSQL.


load_dotenv()
# Cargamos las variables que están dentro del archivo .env.
#
# Por ejemplo, nuestro .env tiene algo parecido a:
#
# DATABASE_URL="postgresql+psycopg://..."
#
# Después de ejecutar load_dotenv(), Python puede acceder
# a esa variable.


DATABASE_URL = os.getenv("DATABASE_URL")
# Buscamos la variable llamada DATABASE_URL.
#
# os.getenv() significa:
# "Dame el valor de esta variable de entorno".
#
# El valor obtenido se guarda en la variable DATABASE_URL.


if not DATABASE_URL:
    # Comprobamos si DATABASE_URL no existe
    # o está vacía.

    raise ValueError("DATABASE_URL no está configurada")
    # Si no encontramos DATABASE_URL, detenemos el programa
    # y mostramos este mensaje de error.
    #
    # Esto nos avisa de que probablemente falta la variable
    # DATABASE_URL en nuestro archivo .env.


engine = create_engine(DATABASE_URL)
# Creamos el engine utilizando nuestra DATABASE_URL.
#
# El engine es el objeto que SQLModel utilizará
# para comunicarse con nuestra base de datos PostgreSQL.
#
# En otras palabras:
#
# .env
#   ↓
# DATABASE_URL
#   ↓
# create_engine()
#   ↓
# engine
#   ↓
# PostgreSQL