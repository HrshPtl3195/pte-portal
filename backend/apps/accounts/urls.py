from django.urls import path
from . import views

urlpatterns = [
    path("pinggg/", views.ping, name="pinggg"),
]
