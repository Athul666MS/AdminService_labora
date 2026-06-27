import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser


class ApplicationListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.APPLICATION_SERVICE_URL}"
                "/api/internal/applications/",
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
                        "Application service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )


class ApplicationDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            application_id
    ):

        try:

            response = requests.get(
                f"{settings.APPLICATION_SERVICE_URL}"
                f"/api/internal/applications/{application_id}/",
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
                        "Application service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )