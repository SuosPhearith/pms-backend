from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("On Hold", "On Hold"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    RISK_LEVEL_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Not Started")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default="low")
    tag = models.CharField(max_length=255, blank=True, null=True)

    backend_percentage = models.IntegerField(default=0)
    frontend_percentage = models.IntegerField(default=0)
    deploy_percentage = models.IntegerField(default=0)
    testing_percentage = models.IntegerField(default=0)
    launch_percentage = models.IntegerField(default=0)

    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_projects")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects_updated")

    deleted_at = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'project'
