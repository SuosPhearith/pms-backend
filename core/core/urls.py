from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/project/', include('project.urls')),
    path('api/task/', include('task.urls')),
    path('api/option/', include('option.urls')),
    path('api/user/', include('user.urls')),
]
