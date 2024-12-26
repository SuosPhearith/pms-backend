from rest_framework.decorators import api_view, permission_classes
from authentication.authorization import IsAdminAndManagerAuthenticated
from rest_framework.response import Response
from rest_framework import status
from authentication.authorization import Roles
from authentication.models import Account
from option.serializers import ManagerSerializer, ProjectOptionSerializer, DeveloperSerializer
from project.models import Project, ProjectDeveloper
from django.db.models import Subquery


@api_view(['GET'])
@permission_classes([IsAdminAndManagerAuthenticated])
def list_managers(request):
    # Get user role
    userId = request.user.id
    userRole = Account.objects.get(user_id = userId)
    if userRole == 'ADMIN':
        managers = Account.objects.filter(role=Roles.manager())
        managers_serializer = ManagerSerializer(managers, many=True)  
        return Response(managers_serializer.data)
    else:
        managers = Account.objects.filter(role=Roles.manager())
        managers_serializer = ManagerSerializer(managers, many=True)  
        return Response(managers_serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminAndManagerAuthenticated])
def list_projects(request):
    # Get user role
    userId = request.user.id
    userRole = Account.objects.get(user_id = userId)
    if userRole.role == 'ADMIN':
        projects = Project.objects.filter(deleted_at = False)
        projects_serializer = ProjectOptionSerializer(projects, many=True)  
        return Response(projects_serializer.data)
    else:
        projects = Project.objects.filter(deleted_at = False, manager_id = userId)
        projects_serializer = ProjectOptionSerializer(projects, many=True)  
        return Response(projects_serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminAndManagerAuthenticated])
def list_developers(request):
    projectId = request.query_params.get('projectId')
    if projectId:
        # Get Devlopers of Project
        projectDevelopers = ProjectDeveloper.objects.filter(project_id=projectId).values('developer_id')
        developers = Account.objects.filter(role=Roles.developer(), user_id__in=Subquery(projectDevelopers))
        developers_serializer = DeveloperSerializer(developers, many=True)  
        return Response(developers_serializer.data)
    else:
        developers = Account.objects.filter(role=Roles.developer())
        developers_serializer = DeveloperSerializer(developers, many=True)  
        return Response(developers_serializer.data)
