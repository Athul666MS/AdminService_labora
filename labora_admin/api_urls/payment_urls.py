from django.urls import path

from labora_admin.views.payment_views import (
    PaymentListView,
    PaymentDetailView,
    PaymentStatsView
)

urlpatterns = [

    path(
        "admin/payments/",
        PaymentListView.as_view()
    ),

    path(
        "admin/payments/stats/",
        PaymentStatsView.as_view()
    ),

    path(
        "admin/payments/<int:payment_id>/",
        PaymentDetailView.as_view()
    ),

]