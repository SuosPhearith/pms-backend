from django.db import models
from django.contrib.auth.models import User
from project.models import Project


class Task(models.Model):
    STAGE_CHOICES = [
        ("Backend", "Backend"),
        ("Frontend", "Frontend"),
        ("Deploy", "Deploy"),
        ("Testing", "Testing"),
        ("Launch", "Launch"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("InProgress", "In Progress"),
        ("done", "Done"),
    ]
    
    STATUS_SUBMIT = [
        ('OnTime', 'On Time'),
        ('late', 'Late'),
    ]
    
    REMARK_STATUS = [
        ('Information', 'Information'),
        ('Suggestion', 'Suggestion'),
        ('Requirement', 'Requirement'),
        ('Unimplement', 'Unimplement'),
    ]


    id              = models.AutoField(primary_key=True)
    project         = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True , related_name="projects")  
    stage           = models.CharField(max_length=20,choices=STAGE_CHOICES,)
    name            = models.CharField(max_length=255)
    description     = models.TextField(blank=True, null=True)
    status          = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending',)
    assigned_to     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    due_at          = models.DateTimeField(null=True, blank=True)
    submited_at     = models.DateTimeField(null=True, blank=True)
    submited_status = models.CharField(max_length=20,choices=STATUS_SUBMIT,null=True, blank=True,)
    
    remark_note     = models.TextField(max_length=400,null=True, blank=True,)
    remark_status   = models.CharField(max_length=20,choices=REMARK_STATUS,null=True, blank=True)
    remark_seen     = models.BooleanField(default=False)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_created")
    updated_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_updated")
    
    deleted_at      = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'task'
