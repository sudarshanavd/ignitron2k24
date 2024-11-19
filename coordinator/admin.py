from django.contrib import admin
from .models import StudentDetail

class StudentDetailAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_lead_name", "contact_number", "institute_name", "district", "event_name")  # Columns to display in the list view
    search_fields = ("team_name", "team_lead_name", "contact_number", "institute_name", "district", "event_name")  # Add search functionality

admin.site.register(StudentDetail, StudentDetailAdmin)
