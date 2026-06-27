import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser
from labora_admin.models import AdminActionLog


def log_admin_action(
        admin_id,
        action,
        target_type,
        target_id,
        description=""
):

    AdminActionLog.objects.create(
        admin_id=admin_id,
        action_type=action,
        target_type=target_type,
        target_id=target_id,
        description=description
    )


class SendNotificationView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def post(self, request):

        user_id = request.data.get(
            "user_id"
        )

        title = request.data.get(
            "title"
        )

        message = request.data.get(
            "message"
        )

        notification_type = request.data.get(
            "notification_type"
        )

        payload = request.data.get(
            "payload",
            {}
        )

        if not all(
            [
                user_id,
                title,
                message,
                notification_type
            ]
        ):

            return Response(
                {
                    "error":
                        "user_id, title, notification_type and message are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            response = requests.post(
                f"{settings.NOTIFICATION_SERVICE_URL}"
                "/api/internal/notifications/create/",
                headers={
                    "X-Service-Key":
                        settings.SERVICE_API_KEY
                },
                json={
                    "user_id": user_id,
                    "type": notification_type,
                    "title": title,
                    "message": message,
                    "payload": payload
                },
                timeout=5
            )

        except requests.RequestException:

            return Response(
                {
                    "error":
                        "Notification service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if response.status_code != status.HTTP_201_CREATED:

            return Response(
                response.json(),
                status=response.status_code
            )

        log_admin_action(
            request.user.id,
            "SEND_NOTIFICATION",
            "user",
            user_id,
            title
        )

        return Response(
            {
                "message":
                    "Notification sent successfully"
            },
            status=status.HTTP_201_CREATED
        )


class BroadcastNotificationView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def post(self, request):

        user_ids = request.data.get(
            "user_ids",
            []
        )

        title = request.data.get(
            "title"
        )

        message = request.data.get(
            "message"
        )

        notification_type = request.data.get(
            "notification_type"
        )

        payload = request.data.get(
            "payload",
            {}
        )

        if not all(
            [
                user_ids,
                title,
                message,
                notification_type
            ]
        ):

            return Response(
                {
                    "error":
                        "user_ids, title, notification_type and message are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            response = requests.post(
                f"{settings.NOTIFICATION_SERVICE_URL}"
                "/api/internal/notifications/broadcast/",
                headers={
                    "X-Service-Key":
                        settings.SERVICE_API_KEY
                },
                json={
                    "user_ids": user_ids,
                    "notification_type": notification_type,
                    "title": title,
                    "message": message,
                    "payload": payload
                },
                timeout=5
            )

        except requests.RequestException:

            return Response(
                {
                    "error":
                        "Notification service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if response.status_code != status.HTTP_201_CREATED:

            return Response(
                response.json(),
                status=response.status_code
            )

        log_admin_action(
            request.user.id,
            "BROADCAST_NOTIFICATION",
            "notification",
            0,
            title
        )

        return Response(
            {
                "message":
                    "Broadcast completed"
            },
            status=status.HTTP_201_CREATED
        )


class NotificationHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.NOTIFICATION_SERVICE_URL}"
                "/api/internal/notifications/",
                headers={
                    "X-Service-Key":
                        settings.SERVICE_API_KEY
                },
                timeout=5
            )

            return Response(
                response.json(),
                status=response.status_code
            )

        except requests.RequestException:

            return Response(
                {
                    "error":
                        "Notification service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )