# apps/core/urls.py
from django.urls import path
from apps.core import views as core_views

urlpatterns = [
    # core test endpoints
    path("settings/list/", core_views.SystemSettingsListView.as_view(), name="core-settings-list"),
    path("settings/get/", core_views.SystemSettingGetView.as_view(), name="core-settings-get"),
    path("settings/create/", core_views.SystemSettingCreateView.as_view(), name="core-settings-create"),
    path("settings/update/", core_views.SystemSettingUpdateView.as_view(), name="core-settings-update"),
    path("settings/delete/", core_views.SystemSettingDeleteView.as_view(), name="core-settings-delete"),

    # keep ping and me under /api/core/ if you prefer; otherwise they remain in project urls
    path("ping/", core_views.PingView.as_view(), name="core-ping"),
    path("me/", core_views.ProtectedMeView.as_view(), name="core-me"),
]
