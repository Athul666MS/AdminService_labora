from django.urls import path

from labora_admin.views.notification_views import (
    SendNotificationView,
    BroadcastNotificationView,
    NotificationHistoryView
)

urlpatterns = [

    path(
        "admin/notifications/send/",
        SendNotificationView.as_view()
    ),

    path(
        "admin/notifications/broadcast/",
        BroadcastNotificationView.as_view()
    ),

    path(
        "admin/notifications/",
        NotificationHistoryView.as_view()
    ),

]