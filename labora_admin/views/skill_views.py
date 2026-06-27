import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser


class SkillListCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        try:

            response = requests.get(
                f"{settings.SKILL_SERVICE_URL}/api/internal/skills/",
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
                        "Skill service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )

    def post(self, request):

        try:

            response = requests.post(
                f"{settings.SKILL_SERVICE_URL}/api/internal/skills/",
                json=request.data,
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
                        "Skill service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )


class SkillDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            skill_id
    ):

        try:

            response = requests.get(
                f"{settings.SKILL_SERVICE_URL}/api/internal/skills/{skill_id}/",
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
                        "Skill service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )

    def put(
            self,
            request,
            skill_id
    ):

        try:

            response = requests.put(
                f"{settings.SKILL_SERVICE_URL}/api/internal/skills/{skill_id}/",
                json=request.data,
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
                        "Skill service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            response.json(),
            status=response.status_code
        )

    def delete(
            self,
            request,
            skill_id
    ):

        try:

            response = requests.delete(
                f"{settings.SKILL_SERVICE_URL}/api/internal/skills/{skill_id}/",
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
                        "Skill service unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if response.status_code == status.HTTP_204_NO_CONTENT:

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            response.json(),
            status=response.status_code
        )