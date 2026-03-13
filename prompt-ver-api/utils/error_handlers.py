from fastapi import Request
from fastapi.responses import JSONResponse

from utils.exceptions import BaseAppException
from utils.logger import logger


async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    logger.warning(
        "Application exception: [%s] %s",
        exc.error_code,
        exc.message,
        extra={"details": exc.details},
    )
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Erro interno do servidor",
            }
        },
    )
