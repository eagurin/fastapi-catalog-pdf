import uvicorn
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, category, document, user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(document.router)
app.include_router(user.router)
