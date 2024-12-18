

from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class ProjectSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'image', 'description', 'start_date', 'end_date', 'status', 
            'priority', 'budget', 'spent', 'risk_level', 'tag', 
            'backend_percentage', 'frontend_percentage', 'deploy_percentage', 
            'testing_percentage', 'launch_percentage', 'manager',
            'created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_at'
        ]
