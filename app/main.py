from fastapi import FastAPI

from app.database import engine
from app.users import models, routers
from app.operations import routers as op_routers

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)
app.include_router(op_routers.router)
