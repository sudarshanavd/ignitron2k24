# coordinator/urls.py
from django.urls import path
from .views import CoordinatorDetailView

app_name = 'coordinator'

urlpatterns = [
    path('<str:event_name>/<str:username>/home/', CoordinatorDetailView.as_view(), name='coordinator_home'),
]
