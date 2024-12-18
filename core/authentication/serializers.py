from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account

# Serializer for User registration (with Account creation)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["ADMIN", "MANAGER", "DEVELOPER"], write_only=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'first_name', 'last_name']

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        if not data.get('first_name'):
            raise serializers.ValidationError({"first_name": "first_name is required"})
        if not data.get('last_name'):
            raise serializers.ValidationError({"last_name": "last_name is required"})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        Account.objects.create(user=user, role=role)  # Create an empty Account for the user
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Serializer for User Account (to be used in the "me" endpoint)
class AccountSerializer(serializers.ModelSerializer):
    user  = UserSerializer()
    class Meta:
        model = Account
        fields = ['user', 'avatar', 'role']
