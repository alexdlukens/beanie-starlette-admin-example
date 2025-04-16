from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette_admin.contrib.beanie import Admin, ModelView
from starlette_admin.views import Link as AdminLink
from starlette_admin import DropDown
from beanie_starlette_admin_example.dependencies import create_db_and_tables
import uvicorn

admin = Admin()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    models = await create_db_and_tables()

    for model in models:
        admin.add_view(ModelView(model, name=model.__name__, icon="database"))

    admin.add_view(
        DropDown(
            "Resources",
            icon="database",
            views=[AdminLink(label="Docs", url="/docs")],
            always_open=False,
        )
    )


    yield


app = FastAPI(lifespan=app_lifespan)
admin.mount_to(app)

if __name__ == "__main__":
    uvicorn.run("beanie_starlette_admin_example.main:app", reload=True)
