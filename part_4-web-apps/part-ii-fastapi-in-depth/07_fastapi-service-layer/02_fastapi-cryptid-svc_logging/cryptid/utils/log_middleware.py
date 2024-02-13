from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

from cryptid.utils.log_json import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "res": {"status_code": response.status_code},
                }
            },
        )
        return response
