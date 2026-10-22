from django.urls import path
from . import climate_alerts
urlpatterns = [
    path('projects/<int:project_id>/resilience/alerts/', climate_alerts.dashboard, name='climate_alerts'),
    path('projects/<int:project_id>/resilience/alerts/chat/', climate_alerts.chat_query, name='chat_query'),
    path('projects/<int:project_id>/resilience/alerts/scenario/', climate_alerts.apply_scenario, name='alert_scenario'),
]
