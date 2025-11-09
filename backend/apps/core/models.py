# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class CoreAuditLog(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    actor_user_id = models.UUIDField(blank=True, null=True)
    actor_service = models.TextField(blank=True, null=True)
    action = models.TextField()
    object_type = models.TextField(blank=True, null=True)
    object_id = models.UUIDField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    ip_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core.core_audit_log'


class CoreSystemSetting(models.Model):
    key = models.TextField(primary_key=True)
    value = models.JSONField()
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'core.core_system_setting'

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True




class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        abstract = True


    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=("is_active", "deleted_at"))


    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=("is_active", "deleted_at"))