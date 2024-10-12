from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controller.mfa_controller import MfaController
from app.view.mfa_view import route

mfa_controller = MfaController()

@asynccontextmanager
async def lifespan(app: FastAPI):
    mfa_controller.scheduler.add_job(
        mfa_controller.update_mfa_code,
        'interval',
        seconds=30
    )

    mfa_controller.scheduler.start()

    yield

    mfa_controller.scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(route)

@app.get('/')
async def home():
    return "Hello, this is the home page of SysAuth"
