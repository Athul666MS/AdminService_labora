import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser


class PaymentListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}"
                "/api/internal/payments/",
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
                        "Payment service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PaymentDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            payment_id
    ):

        try:

            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}"
                f"/api/internal/payments/{payment_id}/",
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
                        "Payment service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PaymentStatsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}"
                "/api/internal/payments/stats/",
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
                        "Payment service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )