# apps/core/serializers.py
from rest_framework import serializers
from typing import Any, Dict

# Try to import the model; if it's missing we still define serializers that are usable
try:
    from apps.core.models import SystemSetting
except Exception:
    SystemSetting = None  # fallback; views will handle missing model at runtime


# Basic response serializer for ping / user summary (kept for schema completeness)
class PingSerializer(serializers.Serializer):
    ping = serializers.CharField()
    request_id = serializers.CharField(allow_null=True)


class UserSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    username = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)
    role = serializers.CharField(allow_null=True)
    is_staff = serializers.BooleanField(default=False)


# -------------------------
# SystemSetting serializers
# -------------------------
if SystemSetting is not None:
    class SystemSettingSerializer(serializers.ModelSerializer):
        class Meta:
            model = SystemSetting
            # adjust fields to match your model, these are common fields
            fields = ["id", "key", "value", "description", "is_deleted", "created_at", "updated_at"]
            read_only_fields = ["id", "created_at", "updated_at", "is_deleted"]
else:
    # fallback plain serializer (schema-only) if model missing
    class SystemSettingSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        key = serializers.CharField()
        value = serializers.CharField(allow_blank=True, allow_null=True)
        description = serializers.CharField(allow_null=True, required=False)
        is_deleted = serializers.BooleanField(default=False, required=False)
        created_at = serializers.DateTimeField(required=False)
        updated_at = serializers.DateTimeField(required=False)


# Request DTOs (POST bodies)
class SystemSettingListRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    page_size = serializers.IntegerField(required=False, min_value=1, default=20)
    query = serializers.CharField(required=False, allow_blank=True)


class SystemSettingGetRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    key = serializers.CharField(required=False, allow_blank=False)

    def validate(self, attrs: Dict[str, Any]):
        if not attrs.get("id") and not attrs.get("key"):
            raise serializers.ValidationError("Either 'id' or 'key' must be provided.")
        return attrs


class SystemSettingCreateSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_key(self, v: str):
        if not v or not v.strip():
            raise serializers.ValidationError("key cannot be empty")
        return v.strip()


class SystemSettingUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    key = serializers.CharField(required=False)
    value = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get("id") and not attrs.get("key"):
            raise serializers.ValidationError("Either 'id' or 'key' must be provided to identify the setting.")
        return attrs


class SystemSettingDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    key = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get("id") and not attrs.get("key"):
            raise serializers.ValidationError("Either 'id' or 'key' must be provided to delete the setting.")
        return attrs
