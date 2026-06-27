from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from labora_admin.permissions import IsAdminUser
from labora_admin.models import AdminActionLog
from labora_admin.serializers import AdminActionLogSerializer


class LogPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class AdminLogsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request):

        logs = AdminActionLog.objects.all()

        action = request.query_params.get(
            "action"
        )

        admin_id = request.query_params.get(
            "admin_id"
        )

        target_type = request.query_params.get(
            "target_type"
        )

        search = request.query_params.get(
            "search"
        )

        if action:

            logs = logs.filter(
                action_type=action
            )

        if admin_id:

            logs = logs.filter(
                admin_id=admin_id
            )

        if target_type:

            logs = logs.filter(
                target_type=target_type
            )

        if search:

            logs = logs.filter(
                Q(description__icontains=search)
                |
                Q(action_type__icontains=search)
            )

        logs = logs.order_by(
            "-created_at"
        )

        paginator = LogPagination()

        paginated_logs = paginator.paginate_queryset(
            logs,
            request
        )

        serializer = AdminActionLogSerializer(
            paginated_logs,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


class AdminLogDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(
        self,
        request,
        log_id
    ):

        try:

            log = AdminActionLog.objects.get(
                id=log_id
            )

        except AdminActionLog.DoesNotExist:

            return Response(
                {
                    "error":
                        "Log not found"
                },
                status=404
            )

        serializer = AdminActionLogSerializer(
            log
        )

        return Response(
            serializer.data
        )