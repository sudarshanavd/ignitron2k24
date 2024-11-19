from django.db import models

class Judge(models.Model):
    judge_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)  
    criteria1 = models.DecimalField(max_digits=5, decimal_places=2)  # For scoring out of 100, e.g., 75.50
    criteria2 = models.DecimalField(max_digits=5, decimal_places=2)
    criteria3 = models.DecimalField(max_digits=5, decimal_places=2)
    criteria4 = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.judge_name} - {self.team_name}"

    class Meta:
        verbose_name = "Judge Detail"
        verbose_name_plural = "Judge Details"
