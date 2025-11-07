# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TestEngineTestsession(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    test_id = models.UUIDField(blank=True, null=True)
    session_type = models.TextField()
    status = models.TextField()
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    current_section = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test_engine.test_engine_testsession'


class TestEngineSessionSection(models.Model):
    id = models.UUIDField(primary_key=True)
    session = models.ForeignKey(TestEngineTestsession, models.DO_NOTHING)
    section_name = models.TextField()
    status = models.TextField()
    time_allowed_seconds = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    result_summary = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test_engine.test_engine_session_section'


class TestEngineSessionLog(models.Model):
    id = models.UUIDField(primary_key=True)
    session = models.ForeignKey(TestEngineTestsession, models.DO_NOTHING, blank=True, null=True)
    actor_user_id = models.UUIDField(blank=True, null=True)
    action = models.TextField()
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test_engine.test_engine_session_log'


class TestEngineSessionLock(models.Model):
    session = models.OneToOneField(TestEngineTestsession, models.DO_NOTHING, primary_key=True)
    locked_by = models.TextField()
    locked_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_engine.test_engine_session_lock'
