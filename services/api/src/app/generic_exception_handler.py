from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger(__name__)

async def generic_exception_handler(request: Request, exc: Exception):
    # Format the exception and its traceback
    exc_traceback = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    
    # Log the formatted exception traceback
    logger.error(msg=exc,extra=request)

    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
