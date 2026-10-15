
from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=120)
    site_version = models.CharField(
        max_length=40,
        default="site-v1",
    )
    site_data = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        VIEWER = "viewer", "Viewer"
        PLANNER = "planner", "Planner"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="unique_project_member",
            )
        ]

    def __str__(self):
        return f"{self.user} / {self.project} / {self.role}"


class Scenario(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=120)
    site_version = models.CharField(max_length=40)
    input_data = models.JSONField()
    result_data = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AuditEvent(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    action = models.CharField(max_length=50)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)