# e_admin/urls.py
from django.urls import path
from .views import AdminDetailView

app_name = 'e_admin'

urlpatterns = [
    path('<str:username>/home/', AdminDetailView.as_view(), name='admin_home'),  # Admin detail page
]
