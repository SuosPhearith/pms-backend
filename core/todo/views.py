from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from task.models import Task
from .serializers import TodoViewOnlySerializer, TodoUpdateStatus
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from authentication.authorization import IsDeveloperAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone


class TodoReadOnlyViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
            return Task.objects.filter(
                deleted_at=False,
                project__deleted_at=False, 
                assigned_to_id=self.request.user.id 
            )
            
    serializer_class = TodoViewOnlySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'stage', 'name', 'description', 'status', 'created_at', 'due_at', 'submited_at', 'submited_status']
    ordering = ['due_at']
    
    filterset_fields = ['stage', 'status', 'project__id']
    
class TodoView(APIView):
    permission_classes = [IsDeveloperAuthenticated]

    def put(self, request):
        serializer = TodoUpdateStatus(data=request.data)
        if serializer.is_valid():
            task = get_object_or_404(Task, id=serializer.validated_data['taskId'])
            if task.assigned_to_id != request.user.id:
                return Response({'message': "This task does not belong to you."}, status=status.HTTP_400_BAD_REQUEST)

            task.status = serializer.validated_data['status']
            if serializer.validated_data['status'] == 'done' :
                task.submited_at = timezone.now()  
            task.submited_status = 'OnTime' if task.due_at > timezone.now() else 'late'
            task.save()

            return Response({"message": "Task status updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 