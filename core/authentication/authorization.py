from rest_framework.permissions import BasePermission
from .models import Account

class IsAdminAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with the 'ADMIN' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has an associated Account and the role is "ADMIN"
        try:
            account = Account.objects.get(user=request.user)
            if account.role == "ADMIN":
                return True
        except Account.DoesNotExist:
            return False
        
        return False
    
class IsAdminAndManagerAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with the 'ADMIN' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has an associated Account and the role is "ADMIN"
        try:
            account = Account.objects.get(user=request.user)
            if account.role == "ADMIN" or account.role == "MANAGER":
                return True
        except Account.DoesNotExist:
            return False
        
        return False
    
class IsManagerAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with the 'MANAGER' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has an associated Account and the role is "MANAGER"
        try:
            account = Account.objects.get(user=request.user)
            if account.role == "MANAGER":
                return True
        except Account.DoesNotExist:
            return False
        
        return False
    
class IsDeveloperAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with the 'DEVELOPER' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has an associated Account and the role is "DEVELOPER"
        try:
            account = Account.objects.get(user=request.user)
            if account.role == "DEVELOPER":
                return True
        except Account.DoesNotExist:
            return False
        
        return False
    
class IsDeveloperAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with the 'DEVELOPER' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has an associated Account and the role is "DEVELOPER"
        try:
            account = Account.objects.get(user=request.user)
            if account.role == "DEVELOPER":
                return True
        except Account.DoesNotExist:
            return False
        
        return False
    
class IsRolesAuthenticated(BasePermission):
    """
    Allows access only to authenticated users with a specific role.
    The roles should be set on the view as `roles`.
    """

    def has_permission(self, request, view):
        # Get the roles from the view
        roles = getattr(view, 'roles', [])

        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Try to get the Account associated with the user
        try:
            if roles.__len__() == 0:
                return True
            account = Account.objects.get(user=request.user)
            # Check if the user's role is in the allowed roles list
            if account.role in roles:
                return True
        except Account.DoesNotExist:
            return False
        
        return False


class Roles:
    @staticmethod
    def admin():
        return "ADMIN"
    
    @staticmethod
    def manager():
        return "MANAGER"
    
    @staticmethod
    def developer():
        return "DEVELOPER"
