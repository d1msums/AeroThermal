from django.urls import path
from . import views
app_name='resilience'
urlpatterns=[
 path('projects/<int:project_id>/resilience/visual-data/',views.visual_data,name='visual_data'),
 path('projects/<int:project_id>/resilience/',views.hub,name='hub'),
 path('projects/<int:project_id>/resilience/view/<slug:audience>/',views.audience,name='audience'),
 path('projects/<int:project_id>/resilience/scenario/',views.scenario,name='scenario'),
 path('projects/<int:project_id>/resilience/snapshot/',views.snapshot,name='snapshot'),
 path('projects/<int:project_id>/resilience/reports/new/',views.report_create,name='report_create'),
 path('projects/<int:project_id>/resilience/reports/<int:report_id>/',views.report_detail,name='report'),
 path('projects/<int:project_id>/resilience/reports/<int:report_id>/triage/',views.triage,name='triage'),
 path('projects/<int:project_id>/resilience/reports/<int:report_id>/photo/',views.photo,name='photo'),
 path('projects/<int:project_id>/resilience/notices/new/',views.publish,name='publish'),
 path('projects/<int:project_id>/resilience/notices/<int:advisory_id>/withdraw/',views.withdraw,name='withdraw'),
 path('projects/<int:project_id>/resilience/map-data/',views.map_data,name='map_data'),
 path('projects/<int:project_id>/resilience/weather/',views.weather,name='weather'),
 path('projects/<int:project_id>/resilience/export/',views.export,name='export'),
]

# AeroThermal Climate Alerts add-on
from .climate_alert_urls import urlpatterns as climate_alert_patterns
urlpatterns += climate_alert_patterns


