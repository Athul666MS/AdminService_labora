from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from labora_admin.permissions import IsAdminUser
from labora_admin.models import (
    PaymentDispute,
    AdminActionLog
)
from labora_admin.serializers import (
    PaymentDisputeSerializer,
    ResolveDisputeSerializer,
    RejectDisputeSerializer
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


class PaymentDisputeListCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        disputes = PaymentDispute.objects.all().order_by(
            "-created_at"
        )

        serializer = PaymentDisputeSerializer(
            disputes,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = PaymentDisputeSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dispute = serializer.save()

        log_admin_action(
            request.user.id,
            "CREATE_DISPUTE",
            "payment",
            dispute.payment_id,
            "Payment dispute created"
        )

        return Response(
            serializer.data,
            status=201
        )


class DisputeDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
            self,
            request,
            dispute_id
    ):

        try:

            dispute = PaymentDispute.objects.get(
                id=dispute_id
            )

        except PaymentDispute.DoesNotExist:

            return Response(
                {
                    "error":
                        "Dispute not found"
                },
                status=404
            )

        serializer = PaymentDisputeSerializer(
            dispute
        )

        return Response(
            serializer.data
        )


class ResolveDisputeView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def patch(
            self,
            request,
            dispute_id
    ):

        try:

            dispute = PaymentDispute.objects.get(
                id=dispute_id
            )

        except PaymentDispute.DoesNotExist:

            return Response(
                {
                    "error":
                        "Dispute not found"
                },
                status=404
            )

        serializer = ResolveDisputeSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dispute.status = "resolved"

        dispute.resolution = serializer.validated_data[
            "resolution"
        ]

        dispute.resolved_by = (
            request.user.id
        )

        dispute.resolved_at = (
            timezone.now()
        )

        dispute.save()

        log_admin_action(
            request.user.id,
            "RESOLVE_DISPUTE",
            "payment",
            dispute.payment_id,
            "Payment dispute resolved"
        )

        return Response(
            PaymentDisputeSerializer(
                dispute
            ).data
        )


class RejectDisputeView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def patch(
            self,
            request,
            dispute_id
    ):

        try:

            dispute = PaymentDispute.objects.get(
                id=dispute_id
            )

        except PaymentDispute.DoesNotExist:

            return Response(
                {
                    "error":
                        "Dispute not found"
                },
                status=404
            )

        serializer = RejectDisputeSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dispute.status = "rejected"

        dispute.resolution = serializer.validated_data[
            "resolution"
        ]

        dispute.resolved_by = (
            request.user.id
        )

        dispute.resolved_at = (
            timezone.now()
        )

        dispute.save()

        log_admin_action(
            request.user.id,
            "REJECT_DISPUTE",
            "payment",
            dispute.payment_id,
            "Payment dispute rejected"
        )

        return Response(
            PaymentDisputeSerializer(
                dispute
            ).data
        )