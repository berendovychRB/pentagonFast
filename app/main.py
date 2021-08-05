from fastapi import FastAPI

import models
# from . import models
from database import engine
# from .database import engine
from routers import user, authentication

# from .routers import user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)

# if __name__ == '__main__':
#     uvicorn.run(app, port=8080, host="0.0.0.0")
