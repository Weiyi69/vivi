from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def error_payload(
    code: str, message: str, request: Request, details: Any = None
) -> dict:
    payload = {
        "code": code,
        "message": message,
        "request_id": getattr(request.state, "request_id", None),
    }
    if details is not None:
        payload["details"] = details
    return payload


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        details = [
            {
                "field": ".".join(str(part) for part in item["loc"]),
                "message": item["msg"],
            }
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=error_payload(
                "validation_error", "Request validation failed", request, details
            ),
        )

    @app.exception_handler(Exception)
    async def unexpected_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_payload(
                "internal_error", "An unexpected server error occurred", request
            ),
        )
