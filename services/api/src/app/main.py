from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.app.logger import setup_logging
from src.ocr.minimum_viable_ocr import minimum_viable_ocr

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
async def ping():
    return "ponk"

@app.get("/mvo")
async def mvo():
    return minimum_viable_ocr()

# Used for logging all uncatched exceptions
app.add_exception_handler(Exception, generic_exception_handler)
