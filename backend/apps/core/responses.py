from rest_framework.response import Response
from rest_framework import status




def ok(data=None, meta=None, status_code=status.HTTP_200_OK):
    payload = {"success": True, "data": data or {}, "meta": meta or {}}
    return Response(payload, status=status_code)




def error(message, code=None, status_code=status.HTTP_400_BAD_REQUEST, details=None):
    payload = {"success": False, "error": {"message": message, "code": code, "details": details}}
    return Response(payload, status=status_code)