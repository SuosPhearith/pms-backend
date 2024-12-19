from rest_framework.routers import DefaultRouter
from .views import TodoReadOnlyViewSet, TodoView
from django.urls import path

# Initialize the router
router = DefaultRouter()
router.register(r'todos-view', TodoReadOnlyViewSet, basename='todo-view')

# Custom URL patterns
urlpatterns = [
    path('update/', TodoView.as_view(), name='todo_view'),
]

# Combine router-generated URLs with custom URLs
urlpatterns += router.urls
