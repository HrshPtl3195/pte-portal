import uuid




def gen_uuid4():
    return str(uuid.uuid4())




def short_code(prefix: str = None) -> str:
    u = uuid.uuid4().hex[:8]
    return f"{prefix}-{u}" if prefix else u