# apps/test_engine/views.py
from typing import Any, Dict, Optional

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers

from apps.core.result import Result, ok, fail

from .services import TestService

try:
    from drf_spectacular.utils import extend_schema, OpenApiResponse
except Exception:
    def extend_schema(*a, **kw):
        def _d(fn):
            return fn
        return _d
    OpenApiResponse = None


class PastResultsSerializer(serializers.Serializer):
    """
    Loose serializer for past results response.
    Each item is treated as a dict so this remains flexible.
    """
    results = serializers.ListField(child=serializers.DictField(), allow_empty=True)
    meta = serializers.DictField(required=False)


class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()


class PastResultsView(APIView):
    """
    POST-only: returns past test results for the authenticated user.

    Defensive rules:
    - If the service raises an exception we return a structured Result.fail with helpful details.
    - If the service returns an object with .to_dict() and that dict already uses the Result envelope,
      we return it as-is.
    - If the service returns unexpected types (or the Result class itself), we detect that and return
      a helpful failure message to make debugging faster.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=PastResultsSerializer) if OpenApiResponse else None}
    )
    def post(self, request, *args, **kwargs):
        svc = TestService(request.user)
        try:
            svc_result = svc.get_past_results()
        except Exception as exc:
            if hasattr(request, "logger"):
                request.logger.exception("TestService.get_past_results() raised an exception")
            exc_type = type(exc).__name__
            exc_msg = str(exc)
            details = {"error": exc_msg, "type": exc_type}
            if "Result" in exc_type or "Result" in exc_msg or "has no attribute 'success'" in exc_msg:
                details["hint"] = "Check TestService: avoid referencing Result.success on the Result class; return a Result instance via Result.ok() or Result.fail()."
            return Response(
                Result.fail(message="Failed to fetch past results", code="service_error", details=details).to_dict(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if isinstance(svc_result, type):
            if hasattr(request, "logger"):
                request.logger.error("Service returned a class/type instead of a result instance", extra={"svc_result_type": str(svc_result)})
            return Response(
                Result.fail(
                    message="Invalid service return type",
                    code="invalid_service_return",
                    details={"hint": "Service returned a class/type instead of an instance. Ensure get_past_results returns a Result instance or serializable dict."}
                ).to_dict(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if hasattr(svc_result, "to_dict") and callable(getattr(svc_result, "to_dict")):
            try:
                payload = svc_result.to_dict()
            except Exception as exc:
                if hasattr(request, "logger"):
                    request.logger.exception("svc_result.to_dict() raised")
                return Response(
                    Result.fail(
                        message="Failed to serialize service result",
                        code="service_serialize_error",
                        details={"error": str(exc)}
                    ).to_dict(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if isinstance(payload, dict) and "success" in payload:
                http_status = status.HTTP_200_OK if payload.get("success", False) else status.HTTP_500_INTERNAL_SERVER_ERROR
                return Response(payload, status=http_status)

            return Response(Result.ok(data=payload).to_dict(), status=status.HTTP_200_OK)

        if hasattr(svc_result, "issucceed"):
            try:
                succeeded = bool(getattr(svc_result, "issucceed"))
            except Exception:
                succeeded = False
            data = getattr(svc_result, "data", None)
            err = getattr(svc_result, "error", None)
            if succeeded:
                return Response(Result.ok(data=data).to_dict(), status=status.HTTP_200_OK)
            else:
                return Response(Result.fail(message="Failed to fetch past results", details={"error": err}).to_dict(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if isinstance(svc_result, (dict, list)):
            return Response(Result.ok(data=svc_result).to_dict(), status=status.HTTP_200_OK)

        try:
            fallback = {"result": str(svc_result)}
        except Exception:
            fallback = {"result": "<unserializable result>"}
        return Response(Result.ok(data=fallback).to_dict(), status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """
    POST-only health endpoint (uniform Result envelope).
    """
    permission_classes = [] 

    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(response=HealthSerializer) if OpenApiResponse else None}
    )
    def post(self, request):
        payload = {"status": "ok", "message": "PTE Portal backend is live"}
        return Response(Result.ok(data=payload).to_dict(), status=status.HTTP_200_OK)
