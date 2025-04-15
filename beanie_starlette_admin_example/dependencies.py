import os
from typing import List

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from beanie_starlette_admin_example.models import Product, Store, Manager

ALL_MODELS = [Product, Store, Manager]

MONGO_URI: str = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE: str = os.environ.get("MONGO_DATABASE", "exampledb")
RECREATE_DB: bool = os.environ.get("RECREATE_DB", "False").lower() == "true"

mongo_client = AsyncIOMotorClient(MONGO_URI)


async def create_db_and_tables() -> List[BaseModel]:
    if RECREATE_DB:
        await mongo_client.drop_database(MONGO_DATABASE)
    await init_beanie(
        database=mongo_client.get_database(MONGO_DATABASE),
        document_models=ALL_MODELS,
    )

    return ALL_MODELS
