# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsUser(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(unique=True)
    password_hash = models.TextField()
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    role = models.ForeignKey('AccountsRole', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts.accounts_user'


class AccountsProfile(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)
    first_name = models.TextField()
    middle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField()
    phone_number = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    locale = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts.accounts_profile'


class AccountsRole(models.Model):
    id = models.UUIDField(primary_key=True)
    key = models.TextField(unique=True)
    name = models.TextField()
    permissions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts.accounts_role'


class AccountsAuthToken(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)
    revoked = models.BooleanField()
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts.accounts_auth_token'


class AccountsAudit(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    event_type = models.TextField()
    success = models.BooleanField()
    ip_address = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts.accounts_audit'
