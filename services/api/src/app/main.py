from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.logging.logger import setup_logging
from src.ocr.minimum_viable_ocr import minimum_viable_ocr

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("app")
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
    ret = await minimum_viable_ocr()
    return ret

# Used for logging all uncatched exceptions
app.add_exception_handler(Exception, generic_exception_handler)
