import requests

from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser
from labora_admin.models import (
    UserVerification,
    AdminActionLog
)
from labora_admin.serializers import (
    UserVerificationSerializer
)


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


class ViewAllUsersView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        headers = {
            "X-Service-Key":
                settings.SERVICE_API_KEY
        }

        data = {
            "clients": [],
            "freelancers": []
        }

        try:

            client_response = requests.get(
                f"{settings.CLIENT_PROFILE_SERVICE_URL}"
                "/api/internal/clients/",
                headers=headers,
                timeout=5
            )

            if client_response.status_code == status.HTTP_200_OK:
                data["clients"] = client_response.json()

        except requests.RequestException:
            pass

        try:

            freelancer_response = requests.get(
                f"{settings.FREELANCER_PROFILE_SERVICE_URL}"
                "/api/internal/freelancers/",
                headers=headers,
                timeout=5
            )

            if freelancer_response.status_code == status.HTTP_200_OK:
                data["freelancers"] = freelancer_response.json()

        except requests.RequestException:
            pass

        return Response(data)


class BlockUserView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def patch(
            self,
            request,
            role,
            user_id
    ):

        try:

            response = requests.patch(
                f"{settings.AUTH_SERVICE_URL}"
                f"/api/internal/users/{user_id}/block/",
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
                        "Auth service unavailable"
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
            "BLOCK_USER",
            "user",
            user_id,
            "User blocked"
        )

        return Response(
            {
                "message":
                    "User blocked successfully"
            },
            status=status.HTTP_200_OK
        )


class UnblockUserView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def patch(
            self,
            request,
            role,
            user_id
    ):

        try:

            response = requests.patch(
                f"{settings.AUTH_SERVICE_URL}"
                f"/api/internal/users/{user_id}/unblock/",
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
                        "Auth service unavailable"
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
            "UNBLOCK_USER",
            "user",
            user_id,
            "User unblocked"
        )

        return Response(
            {
                "message":
                    "User unblocked successfully"
            },
            status=status.HTTP_200_OK
        )


class VerifyUserView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def post(
            self,
            request
    ):

        serializer = UserVerificationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        verification = serializer.save(
            status="verified",
            verified_by=request.user.id,
            verified_at=timezone.now()
        )

        log_admin_action(
            request.user.id,
            "VERIFY_USER",
            "user",
            verification.user_id,
            "User verified"
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )