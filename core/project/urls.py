from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectReadOnlyViewSet, UpdateProgressView
from django.urls import path


router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'projects-list', ProjectReadOnlyViewSet, basename='project-list')

urlpatterns = [
    path('update-progress/', UpdateProgressView.as_view(), name='todo_view'),
]

urlpatterns += router.urls
