from django.db import models


class AdminProfile(models.Model):

    user_id = models.IntegerField(
        unique=True,
        db_index=True
    )

    full_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    is_super_admin = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class UserVerification(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )

    USER_TYPE_CHOICES = (
        ("client", "Client"),
        ("freelancer", "Freelancer"),
    )

    user_id = models.IntegerField(
        unique=True,
        db_index=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    verified_by = models.IntegerField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user_type} "
            f"{self.user_id} "
            f"{self.status}"
        )


class PaymentDispute(models.Model):

    STATUS_CHOICES = (
        ("open", "Open"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    )

    payment_id = models.IntegerField(
        db_index=True
    )

    application_id = models.IntegerField(
        db_index=True
    )

    raised_by = models.IntegerField()

    reason = models.TextField()

    resolution = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    resolved_by = models.IntegerField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Dispute #{self.id}"
        )


class AdminActionLog(models.Model):

    admin_id = models.IntegerField(
        db_index=True
    )

    action_type = models.CharField(
        max_length=100,
        db_index=True
    )

    target_type = models.CharField(
        max_length=50
    )

    target_id = models.IntegerField()

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.action_type} "
            f"by {self.admin_id}"
        ) 