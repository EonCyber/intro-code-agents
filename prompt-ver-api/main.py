from contextlib import asynccontextmanager

import nats
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.routes import router
from messaging.nats_publisher import NATSPublisher
from services.prompt_service import PromptService
from utils.error_handlers import app_exception_handler, generic_exception_handler
from utils.exceptions import BaseAppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    nc = await nats.connect("nats://localhost:4222")
    app.state.prompt_service = PromptService(NATSPublisher(nc))
    yield
    await nc.drain()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.add_exception_handler(BaseAppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


