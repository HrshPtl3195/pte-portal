# apps/core/result.py
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Optional, Dict, Union


@dataclass
class Result:
    """
    Canonical Result envelope used across the project.
    Always serializes to a dict with keys: success, data, error, meta (meta optional).
    """
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "success": bool(self.success),
            "data": self.data if self.data is not None else None,
            "error": self.error if self.error is not None else None,
        }
        if self.meta is not None:
            payload["meta"] = self.meta
        return payload

    @classmethod
    def ok(cls, data: Any = None, meta: Optional[Dict[str, Any]] = None) -> "Result":
        """
        Return a success Result. Use Result.ok(...).to_dict() when returning from views.
        """
        return cls(success=True, data=data, error=None, meta=meta)

    @classmethod
    def fail(cls, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> "Result":
        """
        Return a failure Result with structured error.
        """
        err: Dict[str, Any] = {"message": message}
        if code:
            err["code"] = code
        if details:
            err["details"] = details
        return cls(success=False, data=None, error=err)

    # Optional: make bool(Result) reflect success
    def __bool__(self) -> bool:
        return bool(self.success)


# Backwards-compatible module-level helpers for code calling `from apps.core.result import ok`
def ok(data: Any = None, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return Result.ok(data=data, meta=meta).to_dict()


def fail(message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return Result.fail(message=message, code=code, details=details).to_dict()


# Expose names for from apps.core.result import Result, ok, fail
__all__ = ["Result", "ok", "fail"]
