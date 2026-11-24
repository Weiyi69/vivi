from contextvars import ContextVar
from uuid import uuid4

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestCorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request_id_context.set(request_id)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class TrustedOriginAndCsrfMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, trusted_origins: list[str]):
        super().__init__(app)
        self.trusted_origins = set(trusted_origins)

    async def dispatch(self, request: Request, call_next) -> Response:
        is_auth_mutation = request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
        } and request.url.path.startswith("/api/v1/auth/")
        if is_auth_mutation:
            origin = request.headers.get("Origin")
            referer = request.headers.get("Referer")
            if origin:
                if origin not in self.trusted_origins:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="Untrusted origin"
                    )
            elif referer:
                from urllib.parse import urlparse

                referer_origin = (
                    f"{urlparse(referer).scheme}://{urlparse(referer).netloc}"
                )
                if referer_origin not in self.trusted_origins:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="Untrusted origin"
                    )
            if request.url.path != "/api/v1/auth/csrf":
                csrf_cookie = request.cookies.get("VIVI_CSRF")
                csrf_header = request.headers.get("X-CSRF-Token")
                if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="CSRF validation failed",
                    )
        return await call_next(request)
