from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.app.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(Exception, generic_exception_handler)
