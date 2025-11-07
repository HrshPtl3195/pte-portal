from django.urls import path
from .views import PastResultsView

urlpatterns = [
    path("past-results/", PastResultsView.as_view(), name="past-results"),
]
