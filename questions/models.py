from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    
    def create_user(self, username, password=None, **other_fields):
        if not username:
            raise ValueError("A email must be provided")
        
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, password=None, **other_fields):
        if password is None:
            raise TypeError('Superuser must have password')
                
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user 
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, blank=False, unique=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=128, null=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username
    

class Questions(models.Model):
    """
    the questions model
    """
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False)

    def __str__(self):
        return self.author.username


class Answers(models.Model):
    """
    model of answers to question in questions model  
    """
    question = models.ForeignKey(Questions, blank=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    