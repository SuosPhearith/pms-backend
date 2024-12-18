from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255)  
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    DEVELOPER = 'DEVELOPER'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    ]
    
    role = models.CharField(
        max_length=50,  
        choices=ROLE_CHOICES,
        default=DEVELOPER  
    )

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    class Meta:
        db_table = 'account'
