from django.urls import path

from labora_admin.views.skill_views import (
    SkillListCreateView,
    SkillDetailView,
)

urlpatterns = [

    path(
        "admin/skills/",
        SkillListCreateView.as_view()
    ),

    path(
        "admin/skills/<int:skill_id>/",
        SkillDetailView.as_view()
    ),

]