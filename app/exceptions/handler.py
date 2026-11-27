import logging

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.custom import (
    AppException,
    UnauthorizedException,
    InvalidRefreshTokenError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        prepareResponse: dict = {
            "message": exc.message,
        }
        if exc.data is not None:
            prepareResponse["data"] = exc.data
        return JSONResponse(
            status_code=exc.status_code,
            content=prepareResponse,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.detail),
                "data": None,
                "errors": None,
            },
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = [
            {"field": ".".join(str(x) for x in error["loc"]), "message": error["msg"]}
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=422,
            content={
                "message": "Validation failed",
                "data": None,
                "errors": errors,
            },
        )

    @app.exception_handler(UnauthorizedException)
    async def invalid_token_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidRefreshTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidRefreshTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # logger.exception("Unhandled exception occurred")

        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
            },
        )
