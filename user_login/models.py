from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, mobile_number, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not mobile_number:
            raise ValueError('The Mobile Number field must be set')

        user = self.model(
            username=username,
            mobile_number=mobile_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=15)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    groups = models.ManyToManyField(
        Group,
        related_name='user_login_user_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user_login_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_login_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user_login_user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.username

class Celebrity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
