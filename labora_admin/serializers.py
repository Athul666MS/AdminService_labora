from rest_framework import serializers

from .models import (
    AdminProfile,
    UserVerification,
    PaymentDispute,
    AdminActionLog,
)


class AdminProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AdminProfile

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class UserVerificationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = UserVerification

        fields = "__all__"

        read_only_fields = (
            "id",
            "verified_by",
            "verified_at",
            "created_at",
        )


class PaymentDisputeSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PaymentDispute

        fields = "__all__"

        read_only_fields = (
            "id",
            "status",
            "resolved_by",
            "resolved_at",
            "created_at",
        )

    def validate_reason(
        self,
        value
    ):

        if len(value.strip()) < 10:

            raise serializers.ValidationError(
                "Reason must contain at least 10 characters."
            )

        return value


class ResolveDisputeSerializer(
    serializers.Serializer
):

    resolution = serializers.CharField()


class RejectDisputeSerializer(
    serializers.Serializer
):

    resolution = serializers.CharField()


class AdminActionLogSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AdminActionLog

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
        )


class DashboardStatsSerializer(
    serializers.Serializer
):

    total_clients = serializers.IntegerField()

    total_freelancers = serializers.IntegerField()

    total_jobs = serializers.IntegerField()

    open_jobs = serializers.IntegerField()

    completed_jobs = serializers.IntegerField()

    total_payments = serializers.IntegerField()

    total_reviews = serializers.IntegerField()

    total_revenue = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )