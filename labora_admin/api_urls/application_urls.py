from django.urls import path

from labora_admin.views.application_views import (
    ApplicationListView,
    ApplicationDetailView,
)

urlpatterns = [

    path(
        "admin/applications/",
        ApplicationListView.as_view()
    ),

    path(
        "admin/applications/<int:application_id>/",
        ApplicationDetailView.as_view()
    ),

]