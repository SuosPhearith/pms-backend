from rest_framework import serializers
from task.models import Task
from project.models import Project
from project.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']

class TodoViewOnlySerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only= True)
    created_by = UserSerializer(read_only= True)
    class Meta:
        model = Task
        fields = ['id', 'stage', 'name', 'description', 'status', 'created_at', 'created_by', 'project', 'due_at', 'submited_at', 'submited_status']
        
STATUS_CHOICES = [
    ("pending", "Pending"),
    ("InProgress", "In Progress"),
    ("done", "Done"),
]

class TodoUpdateStatus(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=[choice[0] for choice in STATUS_CHOICES], required=True)