from django.urls import path

from labora_admin.views.user_views import (
    ViewAllUsersView,
    BlockUserView,
    UnblockUserView,
    VerifyUserView
)

urlpatterns = [

    path(
        "admin/users/",
        ViewAllUsersView.as_view()
    ),

    path(
        "admin/users/<str:role>/<int:user_id>/block/",
        BlockUserView.as_view()
    ),

    path(
        "admin/users/<str:role>/<int:user_id>/unblock/",
        UnblockUserView.as_view()
    ),

    path(
        "admin/users/verify/",
        VerifyUserView.as_view()
    ),

]