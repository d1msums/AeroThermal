from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "projects/<int:project_id>/",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "api/projects/<int:project_id>/action/",
        views.run_action,
        name="project_action",
    ),
]