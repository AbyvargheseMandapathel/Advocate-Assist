# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('lawyer', 'Lawyer'),
        ('student', 'Student'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    
    # The is_approved field is only relevant for lawyer accounts
    is_approved = models.BooleanField(default=False, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

