from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    category: str
    stock: int
    description: str


class ProductCreate(SQLModel):
    name: str
    price: float
    category: str
    stock: int
    description: str
