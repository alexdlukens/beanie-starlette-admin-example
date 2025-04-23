import os
from typing import List

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, TypeAdapter
from pathlib import Path
from beanie_starlette_admin_example.models import Product, Store, Manager, Category

ALL_MODELS = [Product, Store, Manager]

MONGO_URI: str = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE: str = os.environ.get("MONGO_DATABASE", "exampledb")
RECREATE_DB: bool = os.environ.get("RECREATE_DB", "False").lower() == "true"

BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" 

mongo_client = AsyncIOMotorClient(MONGO_URI)


async def seed_db() -> None:
    with open(DATA_DIR / "products.json", "r") as file:
        products_data = file.read()
    with open(DATA_DIR / "stores.json", "r") as file:
        stores_data = file.read()
    with open(DATA_DIR / "managers.json", "r") as file:
        managers_data = file.read()
    
    products_adapter = TypeAdapter(List[Product])
    products: List[Product] = products_adapter.validate_json(products_data)
    for product in products:
        product = await product.insert()
        print(product)
    
    stores_adapter = TypeAdapter(List[Store])
    stores: List[Store] = stores_adapter.validate_json(stores_data)
    bestbuy = [store for store in stores if store.name == "Best Buy"][0]
    bestbuy.products.extend([p for p in products if p.category == Category.ELECTRONICS])
    print(bestbuy.products)
    bestbuy = await Store.insert(bestbuy)
    
    walgreens = [store for store in stores if store.name == "Walgreens"][0]
    walgreens.products = [p for p in products if p.category in [Category.BEAUTY, Category.HOME, Category.FASHION]]
    walgreens = await Store.insert(walgreens)
    
    managers_adapter = TypeAdapter(List[Manager])
    manager: Manager = managers_adapter.validate_json(managers_data)[0]
    
    manager.store = bestbuy
    manager = await manager.insert()

async def create_db_and_tables() -> List[BaseModel]:
    if RECREATE_DB:
        await mongo_client.drop_database(MONGO_DATABASE)
    await init_beanie(
        database=mongo_client.get_database(MONGO_DATABASE),
        document_models=ALL_MODELS,
    )
    if RECREATE_DB:
        await seed_db()

    return ALL_MODELS
