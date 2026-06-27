from django.urls import path

from labora_admin.views.review_views import (
    ReviewListView,
    ReviewDetailView,
    DeleteReviewView
)

urlpatterns = [

    path(
        "admin/reviews/",
        ReviewListView.as_view()
    ),

    path(
        "admin/reviews/<int:review_id>/",
        ReviewDetailView.as_view()
    ),

    path(
        "admin/reviews/<int:review_id>/delete/",
        DeleteReviewView.as_view()
    ),

]