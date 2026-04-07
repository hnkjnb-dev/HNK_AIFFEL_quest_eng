"""
요청 로깅 미들웨어
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger_config import setup_logger

logger = setup_logger("request_middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"status={response.status_code} - "
            f"{process_time:.4f}s"
        )
        return response