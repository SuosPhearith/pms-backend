from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.models import Account

class UserReadOnlySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'first_name', 'last_name', 'username', 'email', 'is_active', 'date_joined', 'role']
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_role(self, obj):
        try:
            account = Account.objects.get(user_id=obj.id)
            return account.role
        except Account.DoesNotExist:
            return None
        

class UserUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    role = serializers.CharField(max_length=50 , required = True)
    
    
class UserResetPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(min_length=6, max_length = 100, required=True)
    password2 = serializers.CharField(min_length=6, max_length = 100, required=True)
        