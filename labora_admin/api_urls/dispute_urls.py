from django.urls import path

from labora_admin.views.dispute_views import (
    PaymentDisputeListCreateView,
    ResolveDisputeView,
    RejectDisputeView,
    DisputeDetailView
)

urlpatterns = [

    path(
        "admin/disputes/",
        PaymentDisputeListCreateView.as_view()
    ),

    path(
        "admin/disputes/<int:dispute_id>/",
        DisputeDetailView.as_view()
    ),

    path(
        "admin/disputes/<int:dispute_id>/resolve/",
        ResolveDisputeView.as_view()
    ),

    path(
        "admin/disputes/<int:dispute_id>/reject/",
        RejectDisputeView.as_view()
    ),

]