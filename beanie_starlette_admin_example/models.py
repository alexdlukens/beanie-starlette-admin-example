from beanie import Document,Link
from pydantic import Field, EmailStr, HttpUrl
from enum import Enum

class Category(Enum):
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    HOME = "Home"
    BEAUTY = "Beauty"

class Product(Document):
    name: str = Field(min_length=3, max_length=100)
    description: str
    price: float
    category: Category
    stock: int = Field(ge=0)

class Store(Document):
    name: str = Field(min_length=3, max_length=100)
    location: HttpUrl
    email: EmailStr
    products: list[Link[Product]] = Field(default_factory=list)

class Manager(Document):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    store: Link[Store]
