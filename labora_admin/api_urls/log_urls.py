from django.urls import path

from labora_admin.views.log_views import (
    AdminLogsView,
    AdminLogDetailView
)

urlpatterns = [

    path(
        "admin/logs/",
        AdminLogsView.as_view()
    ),

    path(
        "admin/logs/<int:log_id>/",
        AdminLogDetailView.as_view()
    ),

]