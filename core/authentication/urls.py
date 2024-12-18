from django.urls import path
from .views import hello_view, register_view, login_view, me_view, only_admin_view, role_base_view, token_refresh_view

urlpatterns = [
    path('hello/',       hello_view,            name='hello_view'),
    path('register/',    register_view,         name='register_view'),
    path('refresh/',     token_refresh_view,    name='token_refresh_view'),
    path('login/',       login_view,            name='login_view'),
    path('me/',          me_view,               name='me_view'),
    path('only-admin/',  only_admin_view,       name='only_admin_view'),
    path('role-base/',   role_base_view,        name='role_base_view'),
]
