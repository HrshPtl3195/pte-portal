from typing import Any, Dict, List, Optional
import logging

from apps.core.result import Result

logger = logging.getLogger("apps.test_engine.services")


class TestService:
    def __init__(self, user, request: Optional[Any] = None):
        """
        TestService handles domain logic for the test engine.
        - user: Django user instance
        - request: optional Django request (used only for logging/tracing)
        """
        self.user = user
        self.request = request
        self._log = getattr(request, "logger", logger)

    def get_past_results(self) -> Result:
        """
        Return a Result instance with past results for the user.
        IMPORTANT: always return a Result instance (Result.ok(...) or Result.fail(...)).
        """
        try:
            # === Replace this block with actual ORM queries ===
            # Example placeholder data — replace with real DB queries (PastResult model)
            results: List[Dict[str, Any]] = [
                {"test_id": 1, "score": 78, "date": "2025-11-01"},
                {"test_id": 2, "score": 82, "date": "2025-10-21"},
            ]
            meta = {"count": len(results)}

            return Result.ok(data={"results": results, "meta": meta})

        except Exception as exc:
            try:
                self._log.exception("Error in TestService.get_past_results")
            except Exception:
                logger.exception("Error in TestService.get_past_results (fallback logger)")

            return Result.fail(message="Could not load past results", code="db_error", details={"error": str(exc)})
