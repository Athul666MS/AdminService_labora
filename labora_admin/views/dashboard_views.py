import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser


class DashboardStatsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        headers = {
            "X-Service-Key": settings.SERVICE_API_KEY
        }

        stats = {

            "total_users": 0,
            "total_clients": 0,
            "total_freelancers": 0,

            "total_jobs": 0,
            "open_jobs": 0,
            "in_progress_jobs": 0,
            "completed_jobs": 0,
            "cancelled_jobs": 0,

            "total_applications": 0,

            "total_payments": 0,
            "total_revenue": 0,

            "total_reviews": 0,

        }

        try:

            response = requests.get(
                f"{settings.AUTH_SERVICE_URL}/api/internal/users/stats/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:

                stats.update(
                    response.json()
                )

        except requests.RequestException:
            pass

        try:
            response = requests.get(
                f"{settings.JOB_SERVICE_URL}/api/internal/jobs/stats/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:

                stats.update(
                    response.json()
                )

        except requests.RequestException:
            pass

        try:

            response = requests.get(
                f"{settings.APPLICATION_SERVICE_URL}/api/internal/applications/stats/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:

                stats.update(
                    response.json()
                )

        except requests.RequestException:
            pass

        try:

            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}/api/internal/payments/stats/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:

                stats.update(
                    response.json()
                )

        except requests.RequestException:
            pass

        try:

            response = requests.get(
                f"{settings.REVIEW_SERVICE_URL}/api/internal/reviews/stats/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:

                stats.update(
                    response.json()
                )

        except requests.RequestException:
            pass

        return Response(
            stats
        )