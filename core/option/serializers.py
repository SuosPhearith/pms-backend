from rest_framework import serializers
from authentication.models import Account
from django.contrib.auth.models import User

from project.models import Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id']


class ManagerSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()  
    value = serializers.IntegerField(source='user.id')  

    class Meta:
        model = Account
        fields = ['label', 'value']  

    def get_label(self, obj):
        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        return f"{first_name} {last_name}".strip()

class DeveloperSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()  
    value = serializers.IntegerField(source='user.id')  

    class Meta:
        model = Account
        fields = ['label', 'value']  

    def get_label(self, obj):
        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        return f"{first_name} {last_name}".strip()
    
class ProjectOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField() 
    value = serializers.IntegerField(source='id') 

    class Meta:
        model = Project
        fields = ['label', 'value']  

    def get_label(self, obj):
        name = obj.name or ''
        return f"{name}".strip()

