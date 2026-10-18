from django.contrib import admin
from .models import StakeholderAccess,ClimateState,FieldReport,Advisory
admin.site.register(StakeholderAccess)
# Operational data is managed through project-scoped pages, not generic admin.
