from django.conf import settings
from django.db import models

HAZARDS = [('flood', 'Flood / blocked drainage'), ('heat', 'Heat exposure'),
           ('drought', 'Dry vegetation'), ('wind', 'Wind / fallen branch')]

class StakeholderAccess(models.Model):
    membership = models.OneToOneField('planner.Membership', on_delete=models.CASCADE)
    resident_only = models.BooleanField(default=False)
    def __str__(self):
        return f'Membership {self.membership_id}: resident only={self.resident_only}'

class ClimateState(models.Model):
    project = models.OneToOneField('planner.Project', on_delete=models.CASCADE)
    scenario = models.CharField(max_length=12, default='normal')
    capacity_m3 = models.PositiveIntegerField(default=100000)
    stored_m3 = models.PositiveIntegerField(default=65000)
    reserve_m3 = models.PositiveIntegerField(default=30000)
    target_m3 = models.PositiveIntegerField(default=55000)
    assumed_inflow_m3 = models.PositiveIntegerField(default=0)
    downstream_verified = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=True)
    source = models.CharField(max_length=160, default='Synthetic demonstration inputs; no sensor connection')
    history = models.JSONField(default=list)
    zones = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

class FieldReport(models.Model):
    project = models.ForeignKey('planner.Project', on_delete=models.CASCADE)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    kind = models.CharField(max_length=12, choices=HAZARDS)
    description = models.CharField(max_length=1000)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    photo = models.FileField(upload_to='aerothermal_reports/', blank=True)
    status = models.CharField(max_length=16, default='open', choices=[('open','Open'),('in_progress','In progress'),('resolved','Resolved')])
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='aerothermal_assignments')
    verified = models.BooleanField(default=False)
    demo_points = models.PositiveIntegerField(default=0)
    events = models.JSONField(default=list)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Advisory(models.Model):
    project = models.ForeignKey('planner.Project', on_delete=models.CASCADE)
    kind = models.CharField(max_length=12, choices=HAZARDS)
    title = models.CharField(max_length=120)
    message = models.CharField(max_length=1500)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    active = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=True)
