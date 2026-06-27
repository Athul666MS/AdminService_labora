import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser


class JobListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.JOB_SERVICE_URL}/api/internal/jobs/",
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
                        "Job service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )


class JobDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            job_id
    ):

        try:

            response = requests.get(
                f"{settings.JOB_SERVICE_URL}/api/internal/jobs/{job_id}/",
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
                        "Job service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )