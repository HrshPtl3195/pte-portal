from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.responses import ok
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsAdmin

class PingView(APIView):
    def get(self, request):
        # echo request id to confirm middleware set it
        return ok({"ping": "pong", "request_id": getattr(request, "request_id", None)})


class ProtectedMeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return ok({"user_id": request.user.id, "role": getattr(request.user, "role", None)})
