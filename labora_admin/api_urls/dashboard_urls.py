from django.urls import path

from labora_admin.views.dashboard_views import (
    DashboardStatsView
)

urlpatterns = [

    path(
        "admin/dashboard/",
        DashboardStatsView.as_view()
    ),

]