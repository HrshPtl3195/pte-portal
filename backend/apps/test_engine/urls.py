from django.urls import path
from .views import *

app_name = "test_engine"

urlpatterns = [
    path("past-results/", PastResultsView.as_view(), name="past-results"),
    path("health/", HealthCheckView.as_view(), name="health"),
]
