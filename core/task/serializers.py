from rest_framework import serializers

from project.models import Project
from .models import Task
from project.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'start_date', 'end_date', 'manager', 'created_by', 'priority']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'project', 'name', 'stage', 'due_at', 'submited_at', 'submited_status', 'description', 'status', 'assigned_to', 'created_at', 'updated_at', 'created_by', 'updated_by']
        
        
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'