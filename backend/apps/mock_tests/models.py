# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MockTestsMocktest(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField()
    sections = models.JSONField()
    is_published = models.BooleanField()
    created_by = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mock_tests.mock_tests_mocktest'


class MockTestsQuestion(models.Model):
    id = models.UUIDField(primary_key=True)
    mocktest = models.ForeignKey(MockTestsMocktest, models.DO_NOTHING)
    question_type = models.TextField()
    prompt = models.TextField()
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mock_tests.mock_tests_question'


class MockTestsOption(models.Model):
    id = models.UUIDField(primary_key=True)
    question = models.ForeignKey(MockTestsQuestion, models.DO_NOTHING)
    option_text = models.TextField()
    is_correct = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mock_tests_option'


class MockTestsSubmission(models.Model):
    id = models.UUIDField(primary_key=True)
    mocktest = models.ForeignKey(MockTestsMocktest, models.DO_NOTHING)
    user_id = models.UUIDField()
    session_id = models.UUIDField(blank=True, null=True)
    submission_payload = models.JSONField()
    score = models.JSONField(blank=True, null=True)
    status = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mock_tests_submission'
