from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .authorization import IsAdminAuthenticated, IsRolesAuthenticated, Roles
from .models import Account
from .serializers import RegisterSerializer, AccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView



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

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access'    : str(refresh.access_token),
                'refresh'   : str(refresh)
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
