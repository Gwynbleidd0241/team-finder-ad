from django.shortcuts import redirect
from django.urls import path

from .views import (
    complete_project_view,
    create_project_view,
    project_detail_view,
    project_list_view,
    toggle_participation_view,
    edit_project_view,
    favorite_projects_view,
    toggle_favorite_view,
)
app_name = "projects"

urlpatterns = [
    path("projects/list/", project_list_view, name="list"),
    path("project/list/", lambda request: redirect("projects:list")),
    path("projects/<int:project_id>/", project_detail_view, name="detail"),
    path(
    "projects/<int:project_id>/toggle-participate/",
    toggle_participation_view,
    name="toggle_participate",
    ),
    path(
    "projects/<int:project_id>/complete/",
    complete_project_view,
    name="complete_project",
    ),
    path(
    "projects/create-project/",
    create_project_view,
    name="create_project",
    ),
    path(
    "projects/<int:project_id>/edit/",
    edit_project_view,
    name="edit_project",
    ),
    path("projects/favorites/", favorite_projects_view, name="favorites"),
    path(
    "projects/<int:project_id>/toggle-favorite/",
    toggle_favorite_view,
    name="toggle_favorite",
    ),
]