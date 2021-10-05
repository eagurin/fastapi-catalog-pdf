from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .routers import auth, category, document, user

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(document.router)
app.include_router(user.router)
