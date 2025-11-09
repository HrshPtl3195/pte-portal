# apps/core/middleware.py
import uuid
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from .exceptions import APIError

# module logger
_log = logging.getLogger(__name__)


class RequestIDMiddleware(MiddlewareMixin):
    """
    Attach a request_id to the request and expose a LoggerAdapter at request.logger
    so all logging within the request lifecycle can include request_id.
    """
    header = "HTTP_X_REQUEST_ID"

    def process_request(self, request):
        # reuse incoming X-Request-ID if provided by upstream proxy, otherwise generate one
        request_id = request.META.get(self.header, str(uuid.uuid4()))
        request.request_id = request_id

        # attach a LoggerAdapter bound to this request_id so view/service code can do:
        #    request.logger.info("something")
        # The adapter adds 'request_id' in the extra dict for log records.
        request.logger = logging.LoggerAdapter(_log, {"request_id": request_id})

    def process_response(self, request, response):
        try:
            request_id = getattr(request, "request_id", None)
            if request_id:
                response["X-Request-ID"] = request_id
        except Exception:
            # never allow logging or header-setting to break the response flow
            pass
        return response


class ExceptionToJSONMiddleware(MiddlewareMixin):
    """
    Return JSON for API paths and return HTML debug pages for non-API when DEBUG=True.
    Uses request.logger (if present) so logs include request_id.
    """
    def process_exception(self, request, exception):
        # Always return JSON for API endpoints (paths starting with /api/)
        is_api_path = getattr(request, "path", "").startswith("/api/")

        # If not API and DEBUG is True, let Django show the normal debug HTML page
        if not is_api_path and settings.DEBUG:
            return None

        # choose logger: prefer request-scoped adapter if available
        req_logger = getattr(request, "logger", _log)

        # If it's our known APIError, return its status code and message
        if isinstance(exception, APIError):
            req_logger.warning("APIError occurred: %s", exception, exc_info=exception)
            return JsonResponse(
                {"success": False, "error": {"message": str(exception)}},
                status=getattr(exception, "status_code", 400),
            )

        # For API path or when DEBUG is False, log exception and return generic error
        if is_api_path or not settings.DEBUG:
            # exc_info=True ensures stacktrace is logged; LoggerAdapter passes through extra
            req_logger.exception("Unhandled exception during request: %s", exception)
            return JsonResponse(
                {"success": False, "error": {"message": "Internal Server Error"}},
                status=500,
            )

        # Otherwise, let Django handle it (show debug HTML)
        return None
