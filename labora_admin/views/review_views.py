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


class ReviewListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.REVIEW_SERVICE_URL}"
                "/api/internal/reviews/",
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
                        "Review service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class ReviewDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            review_id
    ):

        try:

            response = requests.get(
                f"{settings.REVIEW_SERVICE_URL}"
                f"/api/internal/reviews/{review_id}/",
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
                        "Review service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class ReviewStatsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.REVIEW_SERVICE_URL}"
                "/api/internal/reviews/stats/",
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
                        "Review service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class DeleteReviewView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def delete(
            self,
            request,
            review_id
    ):

        try:

            response = requests.delete(
                f"{settings.REVIEW_SERVICE_URL}"
                f"/api/internal/reviews/{review_id}/delete/",
                headers={
                    "X-Service-Key":
                        settings.SERVICE_API_KEY
                },
                timeout=5
            )

        except requests.RequestException:

            return Response(
                {
                    "error":
                        "Review service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if response.status_code != status.HTTP_200_OK:

            return Response(
                response.json(),
                status=response.status_code
            )

        log_admin_action(
            request.user.id,
            "DELETE_REVIEW",
            "review",
            review_id,
            "Review deleted by admin"
        )

        return Response(
            {
                "message":
                    "Review deleted successfully"
            },
            status=status.HTTP_200_OK
        )