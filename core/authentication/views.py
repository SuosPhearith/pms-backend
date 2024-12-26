from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .authorization import IsAdminAuthenticated, IsRolesAuthenticated, Roles
from .models import Account
from .serializers import RegisterSerializer, AccountSerializer, UpdateProfileSerializer, UpdatePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password



# Hello View
class Hello(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'message'   : 'User registered successfully',
                'access'    : str(refresh.access_token),
                'refresh'   : str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View (using SimpleJWT)
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username, is_active = True).first()
        if user and user.check_password(password):
            account = Account.objects.get(user_id = user.id)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access'    : str(refresh.access_token),
                'refresh'   : str(refresh),
                'role'      : str(account.role)
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# "Me" View (Get current user's account details)
class MeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user
        account = Account.objects.get(user=user)  # Fetch the user's associated account
        serializer = AccountSerializer(account).data
        return Response({
            "id"            : serializer.get('user').get('id'),
            "username"      : serializer.get('user').get("username"),
            "email"         : serializer.get('user').get("email"),
            "first_name"    : serializer.get('user').get("first_name"),
            "last_name"     : serializer.get('user').get("last_name"),
            "name"          : f"{serializer.get('user').get('first_name')} {serializer.get('user').get('last_name')}",
            "date_joined"   : serializer.get('user').get("date_joined"),
            "role"          : serializer.get('role'),
            "avatar"        : serializer.get('avatar'),
        })
        
class BadAccount(APIView):
    permission_classes = [IsAdminAuthenticated]
    def post(self, request):
        userId = request.data.get('userId')
        if userId:
            infor = False
            user = get_object_or_404(User, id = userId)
            if user.is_active == True:
                infor = False
            else:
                infor = True
            user.is_active = infor
            user.save()
            return Response({'message': "Ban successfully"}, status=status.HTTP_200_OK)
        return Response({'message': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Get the current user
            user = get_object_or_404(User, id=request.user.id)

            # Extract validated data
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            # Check if the email is taken by another user
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'message': "Email is already taken."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the username is taken by another user
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                return Response({'message': "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

            # Update user details
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            return Response({'message': "Profile updated successfully."}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid input.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # Check if the current password is correct
            if not check_password(serializer.validated_data['current_password'], user.password):
                return Response({'message': 'Current password is incorrect.'}, status=400)

            # Update the password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({'message': 'Password updated successfully.'}, status=200)

        return Response(serializer.errors, status=400)

class OnlyAdminView(APIView):
    permission_classes = [IsAdminAuthenticated]
    def get(self, request):
        return Response("You can access")
    
class RoleBaseView(APIView):
    permission_classes = [IsRolesAuthenticated]
    roles = [Roles.admin()]
    def get(seft, request):
        return Response("You can access")
    
# =============== Convert to view ===============

hello_view          = Hello.as_view()
register_view       = RegisterView.as_view()
login_view          = LoginView.as_view()
me_view             = MeView.as_view()
only_admin_view     = OnlyAdminView.as_view()
role_base_view      = RoleBaseView.as_view()
token_refresh_view  = TokenRefreshView.as_view()
bad_account_view    = BadAccount.as_view()
profile_view        = Profile.as_view()