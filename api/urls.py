from django.urls import path
from . import views

urlpatterns = [
    path('missions/', views.mission_list, name='mission-list'),
    path('agent-query/', views.agent_query, name='agent-query'),
    path('process-log/', views.process_log, name='process-log'),
]
