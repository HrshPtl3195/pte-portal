# apps/core/middleware.py
import uuid
import logging
import traceback

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings

from .result import Result
from .exceptions import APIError

logger = logging.getLogger("apps.core.middleware")


class RequestIDMiddleware(MiddlewareMixin):
    """
    Attach a request_id to each request and a logger (LoggerAdapter) that injects it.
    Should be high in MIDDLEWARE order so all downstream code sees request_id.
    """

    def process_request(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id

        # Provide a per-request logger that includes request_id in records.
        request.logger = logging.LoggerAdapter(
            logging.getLogger("apps"),
            {"request_id": request_id},
        )

        # Also set in top-level logger so non-request code can possibly pick it up
        request.logger.debug("Request started", extra={"path": request.path})

    def process_response(self, request, response):
        # ensure response has X-Request-ID header for tracing
        if hasattr(request, "request_id"):
            response.setdefault("X-Request-ID", request.request_id)
        return response


class ExceptionToJSONMiddleware(MiddlewareMixin):
    """
    Catch unhandled exceptions for API routes and return a uniform Result JSON.
    For non-API HTML routes, re-raise / let Django handle depending on DEBUG.
    """

    def process_exception(self, request, exception):
        # If this is not an API path return None so Django's default handlers run.
        # We assume API endpoints are under /api/ — replace if your prefix differs.
        is_api = request.path.startswith("/api/")
        # Prefer using our Result envelope for API responses.
        if is_api:
            # APIError is a controlled error type we can map cleanly
            if isinstance(exception, APIError):
                res = Result.fail(message=str(exception.detail or exception), code=getattr(exception, "code", None))
                status = getattr(exception, "status_code", 400)
                request.logger.exception("Handled APIError") if hasattr(request, "logger") else logger.exception("Handled APIError")
                return JsonResponse(res.to_dict(), status=status)
            # For other exceptions, avoid leaking internals in prod
            if settings.DEBUG:
                # Include traceback when debugging to speed dev
                tb = traceback.format_exc()
                res = Result.fail(message="Internal server error", code="internal_error", details={"traceback": tb})
                request.logger.exception("Unhandled exception in DEBUG") if hasattr(request, "logger") else logger.exception("Unhandled exception in DEBUG")
                return JsonResponse(res.to_dict(), status=500)
            else:
                # Production: minimal info
                request.logger.exception("Unhandled exception") if hasattr(request, "logger") else logger.exception("Unhandled exception")
                res = Result.fail(message="Internal server error", code="internal_error")
                return JsonResponse(res.to_dict(), status=500)
        # not API -> let default flow proceed (return None)
        return None
