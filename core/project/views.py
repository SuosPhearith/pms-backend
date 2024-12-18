
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import Project
from authentication.models import Account
from .serializers import ProjectSerializer
from authentication.authorization import IsAdminAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(ModelViewSet):
    queryset            = Project.objects.filter(deleted_at=False)  # Exclude soft-deleted items
    serializer_class    = ProjectSerializer
    permission_classes  = [IsAdminAuthenticated]
    
    filter_backends     = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields       = ['name', 'description', 'tag']
    ordering_fields     = ['start_date', 'end_date', 'created_at', 'updated_at', 'name', 'description', 'status', 'priority', 'budget', 'spent', 'risk_level' ]  # Fields to order by
    ordering            = ['created_at'] 

    def perform_create(self, serializer):
        manager_id = self.request.data.get('manager_id', None)
        if not manager_id:
            raise ValidationError({"manager_id": "This field is required."})
        is_manager_id = Account.objects.filter(user_id=manager_id, role="MANAGER").exists()
        if not is_manager_id:
            raise ValidationError({"manager_id": "Invalid manager_id."})
        serializer.save(created_by=self.request.user, manager_id=manager_id)


    def perform_update(self, serializer):
        manager_id = self.request.data.get('manager_id', None)
        if not manager_id:
            raise ValidationError({"manager_id": "This field is required."})
        is_manager_id = Account.objects.filter(user_id=manager_id, role="MANAGER").exists()
        if not is_manager_id:
            raise ValidationError({"manager_id": "Invalid manager_id."})
        serializer.save(updated_by=self.request.user, manager_id=manager_id)

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
