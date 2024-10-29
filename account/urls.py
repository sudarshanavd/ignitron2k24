# account/urls.py
from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Single login URL
]
