from dataclasses import dataclass, asdict
from typing import Any, Optional

@dataclass
class Result:
    data: Any = None
    newid: Optional[str] = None
    error: Optional[str] = None
    exception: Optional[str] = None
    token: Optional[str] = None
    message: Optional[str] = None
    issucceed: bool = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def success(cls, data=None, newid=None, message=None, token=None):
        return cls(data=data, newid=newid, message=message, token=token, issucceed=True)

    @classmethod
    def failure(cls, error=None, exception=None, message=None):
        return cls(data=None, error=error, exception=exception, message=message, issucceed=False)
