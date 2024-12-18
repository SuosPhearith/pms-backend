from rest_framework.routers import DefaultRouter
from .views import TaskReadOnlyViewSet, TaskModifyViewSet

router = DefaultRouter()
router.register(r'tasks-view', TaskReadOnlyViewSet, basename='task-view')
router.register(r'tasks', TaskModifyViewSet, basename='task')

urlpatterns = router.urls
