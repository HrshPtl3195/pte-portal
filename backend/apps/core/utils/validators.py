import re
from django.core.exceptions import ValidationError




email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")




def validate_email(value: str):
    if not email_re.match(value):
        raise ValidationError("Invalid email")




def validate_uuid4(value: str):
    import uuid


    try:
        val = uuid.UUID(value, version=4)
    except Exception:
        raise ValidationError("Invalid UUID4")