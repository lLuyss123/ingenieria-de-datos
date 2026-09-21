from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()


class Category(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"

# Field permite configurar restricciones y características de un campo.
# gt significa "greater than" (mayor que).
# Field(gt=0) exige que el valor sea mayor que 0.
# pattern permite validar un texto utilizando una expresión regular.
# La r significa raw string (cadena sin procesar). Permite escribir expresiones regulares con barras invertidas, como \d, sin que Python las interprete previamente.


class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    category: Category
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{3}$")