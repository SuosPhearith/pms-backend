from django.urls import path
from .views import list_managers, list_projects, list_developers

urlpatterns = [
    path('list-managers/',       list_managers,            name='list_managers'),
    path('list-projects/',       list_projects,            name='list_projects'),
    path('list-developers/',     list_developers,          name='list_developers'),
]
