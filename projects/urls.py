from django.urls import path
from .views import (
    project_list_view,
    project_detail_view,
    create_project_view,
    edit_project_view,
    complete_project_view,
    toggle_participate_view,
    skills_autocomplete,
    add_project_skill,
    remove_project_skill,
)

app_name = "projects"

urlpatterns = [
    path("list/", project_list_view, name="project_list"),
    path("create-project/", create_project_view, name="project_create"),
    path("skills/", skills_autocomplete, name="skills_autocomplete"),
    path("<int:pk>/", project_detail_view, name="project_detail"),
    path("<int:pk>/edit/", edit_project_view, name="project_edit"),
    path("<int:pk>/complete/", complete_project_view, name="project_complete"),
    path("<int:pk>/toggle-participate/", toggle_participate_view, name="toggle_participate"),
    path("<int:pk>/skills/add/", add_project_skill, name="add_project_skill"),
    path("<int:pk>/skills/<int:skill_id>/remove/",
         remove_project_skill, name="remove_project_skill"),
]
