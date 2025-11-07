from apps.core.result import Result

class TestService:
    def __init__(self, user):
        self.user = user

    def get_past_results(self) -> Result:
        # placeholder: return empty list for now
        data = [{"test_id": 1, "score": 85, "date_taken": "2025-01-01"}]
        return Result.success(data=data, message="OK")
