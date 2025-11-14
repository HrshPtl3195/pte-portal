from dataclasses import dataclass
from typing import Any, Optional, Dict

@dataclass
class Result:
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to JSON-serializable dict with the uniform envelope.
        {
          "success": True|False,
          "data": ...,
          "error": {"code": "...", "message": "...", "details": {...}} | null,
          "meta": {...} | null
        }
        """
        payload = {
            "success": bool(self.success),
            "data": self.data if self.data is not None else None,
            "error": self.error if self.error is not None else None,
        }
        if self.meta is not None:
            payload["meta"] = self.meta
        return payload

    @staticmethod
    def ok(data: Any = None, meta: Optional[Dict[str, Any]] = None) -> "Result":
        return Result(success=True, data=data, error=None, meta=meta)

    @staticmethod
    def fail(message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> "Result":
        err = {"message": message}
        if code:
            err["code"] = code
        if details:
            err["details"] = details
        return Result(success=False, data=None, error=err)
