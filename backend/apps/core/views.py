# apps/core/views.py
from typing import Any, Dict, Optional

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from apps.core.result import Result
from apps.core.permissions import IsAdmin

# drf-spectacular helpers (safe fallback)
try:
    from drf_spectacular.utils import extend_schema, OpenApiResponse
except Exception:
    def extend_schema(*a, **kw):
        def _d(fn):
            return fn
        return _d
    OpenApiResponse = None

# import serializers
from apps.core.serializers import (
    PingSerializer,
    UserSummarySerializer,
    SystemSettingSerializer,
    SystemSettingListRequestSerializer,
    SystemSettingGetRequestSerializer,
    SystemSettingCreateSerializer,
    SystemSettingUpdateSerializer,
    SystemSettingDeleteSerializer,
)


# ----------------
# utility helpers
# ----------------
def _parse_pagination(body: Dict[str, Any], default_page=1, default_page_size=20):
    try:
        page = int(body.get("page", default_page))
    except Exception:
        page = default_page
    try:
        page_size = int(body.get("page_size", default_page_size))
    except Exception:
        page_size = default_page_size
    return page, page_size


class AdminPageSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 200


# ----------------
# basic core views
# ----------------
class PingView(APIView):
    permission_classes = []  # public

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=PingSerializer) if OpenApiResponse else None
        },
    )
    def post(self, request):
        """
        POST variant of the health-check endpoint, used by newer clients.
        """
        payload = {
            "ping": "pong",
            "request_id": getattr(request, "request_id", None),
        }
        return Response(
            Result.ok(data=payload).to_dict(), status=status.HTTP_200_OK
        )

class ProtectedMeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(request=None, responses={200: OpenApiResponse(response=UserSummarySerializer) if OpenApiResponse else None})
    def post(self, request):
        user = request.user
        user_data = {
            "id": getattr(user, "id", None),
            "username": getattr(user, "username", None),
            "email": getattr(user, "email", None),
            "role": getattr(user, "role", None),
            "is_staff": getattr(user, "is_staff", False),
        }
        return Response(Result.ok(data=user_data).to_dict(), status=status.HTTP_200_OK)


# -------------------------
# SystemSetting CRUD (POST)
# -------------------------
class SystemSettingsListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = AdminPageSizePagination

    @extend_schema(
        request=OpenApiResponse(response=SystemSettingListRequestSerializer) if OpenApiResponse else None,
        responses={200: OpenApiResponse(response=SystemSettingSerializer(many=True)) if OpenApiResponse else None},
    )
    def post(self, request):
        # validate request body
        req_ser = SystemSettingListRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        page_num = req_ser.validated_data.get("page", 1)
        page_size = req_ser.validated_data.get("page_size", 20)
        query = req_ser.validated_data.get("query", "").strip()

        # try to import model; if missing return friendly 501
        try:
            from apps.core.models import SystemSetting
        except Exception as exc:
            return Response(
                Result.fail(
                    message="SystemSetting model not implemented",
                    code="not_implemented",
                    details={"error": str(exc), "hint": "Create apps.core.models.SystemSetting with fields key/value/description"}
                ).to_dict(),
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        qs = SystemSetting.objects.filter(is_deleted=False)
        if query:
            qs = qs.filter(key__icontains=query)

        qs = qs.order_by("key")

        # paginate using DRF paginator
        paginator = self.pagination_class()
        # trick: set query params so paginator works with POST body pagination
        request._request.GET = request._request.GET.copy()
        request._request.GET["page"] = str(page_num)
        request._request.GET["page_size"] = str(page_size)

        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = SystemSettingSerializer(page, many=True, context={"request": request})
        meta = {
            "count": paginator.page.paginator.count if getattr(paginator, "page", None) else len(serializer.data),
            "page": page_num,
            "page_size": page_size,
        }
        return Response(Result.ok(data=serializer.data, meta=meta).to_dict(), status=status.HTTP_200_OK)


class SystemSettingGetView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=OpenApiResponse(response=SystemSettingGetRequestSerializer) if OpenApiResponse else None,
        responses={200: OpenApiResponse(response=SystemSettingSerializer) if OpenApiResponse else None},
    )
    def post(self, request):
        req_ser = SystemSettingGetRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        data = req_ser.validated_data

        try:
            from apps.core.models import SystemSetting
        except Exception as exc:
            return Response(
                Result.fail(
                    message="SystemSetting model not implemented",
                    code="not_implemented",
                    details={"error": str(exc), "hint": "Create apps.core.models.SystemSetting"}
                ).to_dict(),
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        obj = None
        if "id" in data:
            obj = SystemSetting.objects.filter(id=data["id"], is_deleted=False).first()
        elif "key" in data:
            obj = SystemSetting.objects.filter(key=data["key"], is_deleted=False).first()

        if not obj:
            return Response(Result.fail(message="SystemSetting not found", code="not_found").to_dict(), status=status.HTTP_404_NOT_FOUND)

        serializer = SystemSettingSerializer(obj, context={"request": request})
        return Response(Result.ok(data=serializer.data).to_dict(), status=status.HTTP_200_OK)


class SystemSettingCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=OpenApiResponse(response=SystemSettingCreateSerializer) if OpenApiResponse else None,
        responses={201: OpenApiResponse(response=SystemSettingSerializer) if OpenApiResponse else None},
    )
    def post(self, request):
        req_ser = SystemSettingCreateSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        data = req_ser.validated_data

        try:
            from apps.core.models import SystemSetting
        except Exception as exc:
            return Response(
                Result.fail(
                    message="SystemSetting model not implemented",
                    code="not_implemented",
                    details={"error": str(exc), "hint": "Create apps.core.models.SystemSetting"}
                ).to_dict(),
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        # Prevent duplicate keys
        if SystemSetting.objects.filter(key=data["key"]).exists():
            return Response(Result.fail(message="SystemSetting with this key already exists", code="conflict").to_dict(), status=status.HTTP_409_CONFLICT)

        # Create (use transaction for safety)
        with transaction.atomic():
            obj = SystemSetting.objects.create(
                key=data["key"],
                value=data.get("value"),
                description=data.get("description"),
            )
        serializer = SystemSettingSerializer(obj, context={"request": request})
        return Response(Result.ok(data=serializer.data).to_dict(), status=status.HTTP_201_CREATED)


class SystemSettingUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=OpenApiResponse(response=SystemSettingUpdateSerializer) if OpenApiResponse else None,
        responses={200: OpenApiResponse(response=SystemSettingSerializer) if OpenApiResponse else None},
    )
    def post(self, request):
        req_ser = SystemSettingUpdateSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        data = req_ser.validated_data

        try:
            from apps.core.models import SystemSetting
        except Exception as exc:
            return Response(
                Result.fail(
                    message="SystemSetting model not implemented",
                    code="not_implemented",
                    details={"error": str(exc), "hint": "Create apps.core.models.SystemSetting"}
                ).to_dict(),
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        obj = None
        if data.get("id"):
            obj = SystemSetting.objects.filter(id=data["id"], is_deleted=False).first()
        elif data.get("key"):
            obj = SystemSetting.objects.filter(key=data["key"], is_deleted=False).first()

        if not obj:
            return Response(Result.fail(message="SystemSetting not found", code="not_found").to_dict(), status=status.HTTP_404_NOT_FOUND)

        # Apply partial updates
        changed = False
        if "value" in data:
            obj.value = data["value"]
            changed = True
        if "description" in data:
            obj.description = data["description"]
            changed = True
        if "key" in data and data["key"] != obj.key:
            # ensure new key uniqueness
            if SystemSetting.objects.filter(key=data["key"]).exclude(id=obj.id).exists():
                return Response(Result.fail(message="SystemSetting key conflict", code="conflict").to_dict(), status=status.HTTP_409_CONFLICT)
            obj.key = data["key"]
            changed = True

        if changed:
            obj.save()

        serializer = SystemSettingSerializer(obj, context={"request": request})
        return Response(Result.ok(data=serializer.data).to_dict(), status=status.HTTP_200_OK)


class SystemSettingDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=OpenApiResponse(response=SystemSettingDeleteSerializer) if OpenApiResponse else None,
        responses={200: OpenApiResponse(response=SystemSettingSerializer) if OpenApiResponse else None},
    )
    def post(self, request):
        req_ser = SystemSettingDeleteSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        data = req_ser.validated_data

        try:
            from apps.core.models import SystemSetting
        except Exception as exc:
            return Response(
                Result.fail(
                    message="SystemSetting model not implemented",
                    code="not_implemented",
                    details={"error": str(exc), "hint": "Create apps.core.models.SystemSetting"}
                ).to_dict(),
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        obj = None
        if data.get("id"):
            obj = SystemSetting.objects.filter(id=data["id"], is_deleted=False).first()
        elif data.get("key"):
            obj = SystemSetting.objects.filter(key=data["key"], is_deleted=False).first()

        if not obj:
            return Response(Result.fail(message="SystemSetting not found", code="not_found").to_dict(), status=status.HTTP_404_NOT_FOUND)

        # Soft delete: set is_deleted flag if present, otherwise delete
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = True
            obj.save()
        else:
            obj.delete()

        serializer = SystemSettingSerializer(obj, context={"request": request})
        return Response(Result.ok(data=serializer.data).to_dict(), status=status.HTTP_200_OK)
