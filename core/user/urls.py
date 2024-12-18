from rest_framework.routers import DefaultRouter
from .views import UserReadOnlyViewSet, user_view
from django.urls import path

# Initialize the router
router = DefaultRouter()
router.register(r'users-view', UserReadOnlyViewSet, basename='users-view')

# Custom URL patterns
urlpatterns = [
    path('update/', user_view, name='user_view'),
]

# Combine router-generated URLs with custom URLs
urlpatterns += router.urls
