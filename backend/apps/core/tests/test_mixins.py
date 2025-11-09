import pytest
from django.utils import timezone
from core.models import TimestampedModel




class Dummy(TimestampedModel):
    class Meta:
        app_label = "core"




def test_timestamped_model_fields(db):
    d = Dummy.objects.create()
    assert d.created_at is not None
    assert d.updated_at is not None
    assert d.created_at <= timezone.now()