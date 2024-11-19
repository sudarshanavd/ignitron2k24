from django.contrib import admin
from .models import Judge

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('judge_name', 'team_name','event_name', 'criteria1', 'criteria2', 'criteria3','criteria4')
    search_fields = ('judge_name', 'team_name','event_name')

