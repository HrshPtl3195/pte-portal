from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import TestService
from rest_framework import status


class PastResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        svc = TestService(request.user)
        result = svc.get_past_results()
        status_code = 200 if result.issucceed else 500
        return Response(result.to_dict(), status=status_code)


class HealthCheckView(APIView):
    permission_classes = []  # open endpoint for now

    def get(self, request):
        return Response({"status": "ok", "message": "PTE Portal backend is live"}, status=status.HTTP_200_OK)
