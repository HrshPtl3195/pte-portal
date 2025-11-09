
# apps/core/exceptions.py (append)
from rest_framework.views import exception_handler as drf_exception_handler_orig
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status




class APIError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A server error occurred."
    default_code = "error"


    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail or self.default_detail, code or self.default_code)




class PermissionDeniedError(APIError):
    def __init__(self, detail="Permission denied"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


def drf_exception_handler(exc, context):
    """
    Wrap DRF's exception handler into our JSON envelope.
    """
    drf_resp = drf_exception_handler_orig(exc, context)
    if drf_resp is None:
        return None

    # drf_resp.data is usually a dict; try to extract a friendly message
    data = drf_resp.data
    msg = None
    if isinstance(data, dict):
        # common DRF shapes: {'detail': '...'} or field-errors dict
        msg = data.get("detail") or "Validation error"
    else:
        msg = str(data)

    return Response(
        {"success": False, "error": {"message": msg, "details": data}},
        status=drf_resp.status_code,
    )
