from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import AccountManager

class Account(AbstractBaseUser, PermissionsMixin):
    """
    Account model using email for authentication instead of a traditional username.
    """

    profile_id = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True)

    is_staff = models.BooleanField(default=False)                   # For admin site access.
    is_superuser = models.BooleanField(default=False)               # For all-encompassing permissions.
    is_active = models.BooleanField(default=True)                   # For account activation status.

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self):
        return str(self.profile_id)
    
