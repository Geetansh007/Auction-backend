from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    

class Celebrity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
