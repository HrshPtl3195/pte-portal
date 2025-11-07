from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import TestService

class PastResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        svc = TestService(request.user)
        result = svc.get_past_results()
        status_code = 200 if result.issucceed else 500
        return Response(result.to_dict(), status=status_code)
