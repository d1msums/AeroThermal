from django.contrib import admin
from .models import Project, Membership


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "site_version")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "role")
    list_filter = ("role",)