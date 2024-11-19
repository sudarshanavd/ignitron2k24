# judge/urls.py
from django.urls import path
from .views import JudgeDetailView,JudgeEvaluationView

app_name = 'judge'

urlpatterns = [
    path('<str:event_name>/<str:username>/home/', JudgeDetailView.as_view(), name='judge_home'),
    path('<str:event_name>/<str:username>/<str:team_name>/evaluation/', JudgeEvaluationView.as_view(), name='judge_evaluation'),
]