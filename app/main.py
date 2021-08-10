from fastapi import FastAPI

from app.database import engine
from app.users import authentication, models, routers

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(routers.router)
app.include_router(authentication.router)
