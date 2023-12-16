from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class AccountManager(BaseUserManager):
    """
    A specialised manager for `Account` model to include additional functionalities such as creating admin users.

    Inherits from `BaseUserManager` which offers utility methods for handling user object creation, specifically
    beneficial when utilising custom user models.
    """

    def create_user(self, email, username, fullname, password, **additional_fields):
        """
        Generates and returns a normal user with specified email, username, fullname, and password.
        """

        # Verifying email and username are provided.
        if not email:
            raise ValueError(_('An email address is required.'))

        if not username:
            raise ValueError(_('A username is required.'))

        # Normalising the email.
        email = self.normalize_email(email)

        # User creation
        user = self.model(email=email, username=username, fullname=fullname, **additional_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, username, fullname, password, **additional_fields):
        """
        Generates and returns an admin user with specified email, username, fullname, and password.
        """

        # Setting user attributes for staff and superuser status.
        additional_fields.setdefault('is_staff', True)
        additional_fields.setdefault('is_superuser', True)
        additional_fields.setdefault('is_active', True)

        # Validating the staff and superuser status.
        if not additional_fields.get('is_staff') or not additional_fields.get('is_superuser'):
            raise ValueError('Admin user requires both is_staff=True and is_superuser=True.')

        return self.create_user(email, username, fullname, password, **additional_fields)

    
    
