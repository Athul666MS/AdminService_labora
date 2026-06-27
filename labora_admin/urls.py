from django.urls import path, include
urlpatterns = [
    path("", include("labora_admin.api_urls.dashboard_urls")),
    path("", include("labora_admin.api_urls.user_urls")),
    path("", include("labora_admin.api_urls.dispute_urls")),
    path("", include("labora_admin.api_urls.payment_urls")),
    path("", include("labora_admin.api_urls.review_urls")),
    path("", include("labora_admin.api_urls.notification_urls")),
    path("", include("labora_admin.api_urls.log_urls")),
path("", include("labora_admin.api_urls.job_urls")),
path("", include("labora_admin.api_urls.skill_urls")),
path("", include("labora_admin.api_urls.application_urls")),
]