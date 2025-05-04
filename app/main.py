from fastapi import FastAPI
from .routes import router
from .login import router_login

app = FastAPI()
app.include_router(router)
app.include_router(router_login)