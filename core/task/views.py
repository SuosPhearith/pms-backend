from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskFilter
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from authentication.models import Account
from django.contrib.auth.models import User
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class TaskReadOnlyViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        account = get_object_or_404(Account, user_id = self.request.user.id)
        if account.role == 'MANAGER':
            return Task.objects.filter(deleted_at=False, project__deleted_at=False, project__manager_id = self.request.user.id)
        else:
            return Task.objects.filter(deleted_at=False, project__deleted_at=False)
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'project', 'submited_status', 'name', 'stage','due_at','submited_at', 'description', 'status', 'assigned_to', 'created_at', 'updated_at', 'created_by', 'updated_by']
    ordering = ['created_at']

    filterset_class = TaskFilter


class TaskModifyViewSet(ModelViewSet):
    queryset = Task.objects.filter(deleted_at=False)
    serializer_class = TaskCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        assigned_to = self.request.data.get('assigned_to', None)
        if not assigned_to:
            raise ValidationError({"assigned_to": "This field is required."})
        is_assigned_to = Account.objects.filter(user_id=assigned_to, role="DEVELOPER").exists()
        if not is_assigned_to:
            raise ValidationError({"assigned_to": "Invalid assigned_to."})

        developer_instance = User.objects.get(id=assigned_to)
        serializer.save(created_by=self.request.user, assigned_to=developer_instance)
        
    @action(detail=False, methods=['DELETE'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', None)
        if not ids or not isinstance(ids, list):
            return Response({"error": "A list of Task IDs is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        updated_count = Task.objects.filter(id__in=ids, deleted_at=False).update(deleted_at=True)
        return Response(
            {"message": "Deleted Successfully"},
            status=status.HTTP_200_OK
        )

