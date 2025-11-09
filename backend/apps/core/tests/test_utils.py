from apps.core.utils.id_helpers import gen_uuid4
from apps.core.utils.time_helpers import now_utc
import uuid

def test_gen_uuid4():
    u = gen_uuid4()
    assert len(u) == 36

def test_uuid4_length():
    u = gen_uuid4()
    assert len(u) == 36
    uuid.UUID(u)  # should not raise

def test_now_utc():
    import datetime
    n = now_utc()
    assert n.tzinfo is not None
    assert isinstance(n, datetime.datetime)
