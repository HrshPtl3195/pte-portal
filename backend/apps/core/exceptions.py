# apps/core/exceptions.py
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_default_handler
from rest_framework.response import Response
from rest_framework import status

from .result import Result


class APIError(APIException):
    """
    Generic application-level API error. Use this when you want a controlled JSON error.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request"
    default_code = "api_error"


class PermissionDeniedError(APIError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied"
    default_code = "permission_denied"


def drf_exception_handler(exc, context):
    """
    Wrap DRF exceptions into the uniform Result envelope.
    Use in settings: REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'apps.core.exceptions.drf_exception_handler'
    """
    # Let DRF produce its standard response first (gives status_code & body we can reuse)
    drf_resp = drf_default_handler(exc, context)
    if drf_resp is None:
        # Not handled by DRF's default handler -> produce generic internal error shape
        res = Result.fail(message="Internal server error", code="internal_error")
        return Response(res.to_dict(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # If DRF returned a Response, convert its data into our Result envelope
    status_code = drf_resp.status_code
    data = drf_resp.data

    # If data is already shaped as our envelope (avoid double-wrapping)
    if isinstance(data, dict) and ("success" in data and ("data" in data or "error" in data)):
        return drf_resp

    # Build error info when status >= 400
    if 400 <= status_code < 600:
        # DRF often returns {'detail': '...'} or field-errors dict
        if isinstance(data, dict) and "detail" in data:
            message = data.get("detail")
            err = {"message": message}
        else:
            # validation errors or other structured errors
            err = {"message": "Validation error", "details": data} if status_code == 400 else {"message": data}
        res = Result.fail(message=err.get("message", "Error"), code=None, details=err.get("details"))
        return Response(res.to_dict(), status=status_code)

    # For anything else (2xx) — return as success
    res = Result.ok(data=data)
    return Response(res.to_dict(), status=status_code)
