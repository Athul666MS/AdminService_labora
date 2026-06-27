from django.urls import path

from labora_admin.views.job_views import (
    JobListView,
    JobDetailView,
)

urlpatterns = [

    path(
        "admin/jobs/",
        JobListView.as_view()
    ),

    path(
        "admin/jobs/<int:job_id>/",
        JobDetailView.as_view()
    ),

]