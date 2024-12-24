
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from .models import Project, ProjectDeveloper
from authentication.models import Account
from .serializers import ProjectSerializer, ProjectReadOnlySerializer, UpdateProgressSerializer
from authentication.authorization import IsAdminAuthenticated, IsManagerAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db import transaction




class ProjectReadOnlyViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        return Project.objects.filter(
            deleted_at=False,
            manager_id=self.request.user.id 
        )
    serializer_class    = ProjectReadOnlySerializer
    permission_classes  = [AllowAny]
    
    filter_backends     = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields       = ['name', 'description', 'tag']
    ordering_fields     = ['start_date', 'end_date', 'name', 'description', 'status', 'priority', 'risk_level' ]  # Fields to order by
    ordering            = ['created_at']
    
    filterset_fields = ['status']

class UpdateProgressView(APIView):
    permission_classes = [IsManagerAuthenticated]
    def patch(self, request):
        serializer = UpdateProgressSerializer(data=request.data)
        if serializer.is_valid():
            project = get_object_or_404(Project, id=serializer.validated_data['id'])
            if project.manager_id != request.user.id:
                return Response({'message': "This project does not belong to you."}, status=status.HTTP_400_BAD_REQUEST)
            project.backend_percentage = serializer.validated_data['backend_percentage']
            project.frontend_percentage = serializer.validated_data['frontend_percentage']
            project.deploy_percentage = serializer.validated_data['deploy_percentage']
            project.testing_percentage = serializer.validated_data['testing_percentage']
            project.launch_percentage = serializer.validated_data['launch_percentage']
            project.save()
            return Response({"message": "Project status updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(ModelViewSet):
    queryset            = Project.objects.filter(deleted_at=False)  # Exclude soft-deleted items
    serializer_class    = ProjectSerializer
    permission_classes  = [IsAdminAuthenticated]
    
    filter_backends     = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields       = ['name', 'description', 'tag']
    ordering_fields     = ['start_date', 'end_date', 'created_at', 'updated_at', 'name', 'description', 'status', 'priority', 'budget', 'spent', 'risk_level' ]  # Fields to order by
    ordering            = ['created_at'] 
    
    filterset_fields = ['status']

    def perform_create(self, serializer):
        with transaction.atomic():
            # Validate manager_id
            manager_id = self.request.data.get('manager_id')
            if not manager_id:
                raise ValidationError({"manager_id": "This field is required."})
            
            is_manager_valid = Account.objects.filter(user_id=manager_id, role="MANAGER").exists()
            if not is_manager_valid:
                raise ValidationError({"manager_id": "Invalid manager_id."})
            
            # Save project with manager_id and created_by
            project = serializer.save(created_by=self.request.user, manager_id=manager_id)
            
            # Validate and add developers
            dev_ids = self.request.data.get('dev_ids', [])
            if not isinstance(dev_ids, list):
                raise ValidationError({"dev_ids": "This field must be a list of developer IDs."})
            
            if dev_ids:
                developers = []
                for dev_id in dev_ids:
                    # Validate each developer ID
                    account = get_object_or_404(Account, user_id=dev_id)
                    if account.role != "DEVELOPER":
                        return Response({"message": f"Invalid Developer ID: {dev_id}"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Get the User instance and prepare for bulk creation
                    developer_user = User.objects.get(id=account.user_id)
                    developers.append(ProjectDeveloper(developer=developer_user, project=project))
                
                # Bulk create to optimize database interactions
                ProjectDeveloper.objects.bulk_create(developers)
        


    def perform_update(self, serializer):
        with transaction.atomic():
            manager_id = self.request.data.get('manager_id', None)
            if not manager_id:
                raise ValidationError({"manager_id": "This field is required."})
            is_manager_id = Account.objects.filter(user_id=manager_id, role="MANAGER").exists()
            if not is_manager_id:
                raise ValidationError({"manager_id": "Invalid manager_id."})
            project = serializer.save(updated_by=self.request.user, manager_id=manager_id)
            dev_ids = self.request.data.get('dev_ids', [])
            if not isinstance(dev_ids, list):
                raise ValidationError({"dev_ids": "This field must be a list of developer IDs."})
            
            if dev_ids:
                # delete old
                ProjectDeveloper.objects.filter(project_id=project.id).delete()
                developers = []
                for dev_id in dev_ids:
                    # Validate each developer ID
                    account = get_object_or_404(Account, user_id=dev_id)
                    if account.role != "DEVELOPER":
                        return Response({"message": f"Invalid Developer ID: {dev_id}"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Get the User instance and prepare for bulk creation
                    developer_user = User.objects.get(id=account.user_id)
                    developers.append(ProjectDeveloper(developer=developer_user, project=project))
                
                # Bulk create to optimize database interactions
                ProjectDeveloper.objects.bulk_create(developers)

    def perform_destroy(self, instance):
        instance.deleted_at = True
        instance.save()
        
    @action(detail=False, methods=['DELETE'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', None)
        if not ids or not isinstance(ids, list):
            return Response({"error": "A list of project IDs is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        updated_count = Project.objects.filter(id__in=ids, deleted_at=False).update(deleted_at=True)
        return Response(
            {"message": "Deleted Successfully"},
            status=status.HTTP_200_OK
        )
