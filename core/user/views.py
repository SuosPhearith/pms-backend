from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.models import User
from .serializers import UserReadOnlySerializer, UserUpdateSerializer, UserResetPasswordSerializer
from rest_framework.permissions import AllowAny
from authentication.authorization import IsAdminAuthenticated

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from authentication.models import Account
from django.db import transaction





class UserReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True, is_superuser=False)
    serializer_class = UserReadOnlySerializer
    permission_classes = [IsAdminAuthenticated]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering_fields = ['id', 'date_joined' , 'email', 'username',]
    ordering = ['date_joined']
    
    # filterset_fields = ['role']


class UserView(APIView):
    permission_classes = [IsAdminAuthenticated]

    @transaction.atomic
    def put(self, request):
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Access the ID from validated data
            user_id = serializer.validated_data['id']

            # Fetch the Account and User objects
            account = get_object_or_404(Account, user_id=user_id)
            user = get_object_or_404(User, id=user_id)

            # Update the Account fields
            account.role = serializer.validated_data['role']
            account.save()

            # Update the User fields
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.username = serializer.validated_data['username']
            user.email = serializer.validated_data['email']
            user.save()

            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def patch(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] != serializer.validated_data['password2']:
                return Response({'message': "Invalid Confirm Password"}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, id=serializer.validated_data['id'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

user_view = UserView.as_view()