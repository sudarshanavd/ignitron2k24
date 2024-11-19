from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError

class StudentDetail(models.Model):
    team_name = models.CharField(max_length=100)
    team_lead_name = models.CharField(max_length=100)
    contact_number = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")],
    )
    event_name = models.CharField(max_length=100,)
    institute_name = models.CharField(max_length=150)
    district = models.CharField(max_length=100)
    
    # Additional participants
    participant_2 = models.CharField(max_length=100, blank=True, null=True)
    participant_3 = models.CharField(max_length=100, blank=True, null=True)
    participant_4 = models.CharField(max_length=100, blank=True, null=True)
    
    # Optional task description field
    task = models.TextField(blank=True, null=True)
    
    def clean(self):
        for field in ["team_name", "team_lead_name", "contact_number", "event_name", "institute_name", "district"]:
            if not getattr(self, field):
                raise ValidationError({field: f"{field.replace('_', ' ').capitalize()} is required."})

    
    def __str__(self):
        return f"{self.team_name} - {self.team_lead_name}"

    class Meta:
        verbose_name = "Student Detail"
        verbose_name_plural = "Student Details"
