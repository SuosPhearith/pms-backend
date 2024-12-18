from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from authentication.authorization import Roles
from authentication.models import Account
from option.serializers import ManagerSerializer, ProjectOptionSerializer, DeveloperSerializer
from project.models import Project

@api_view(['GET'])
def list_managers(request):
    managers = Account.objects.filter(role=Roles.manager())
    managers_serializer = ManagerSerializer(managers, many=True)  
    return Response(managers_serializer.data)


@api_view(['GET'])
def list_projects(request):
    projects = Project.objects.filter(deleted_at = False)
    projects_serializer = ProjectOptionSerializer(projects, many=True)  
    return Response(projects_serializer.data)


@api_view(['GET'])
def list_developers(request):
    developers = Account.objects.filter(role=Roles.developer())
    developers_serializer = DeveloperSerializer(developers, many=True)  
    return Response(developers_serializer.data)
