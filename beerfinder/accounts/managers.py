from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """

        if not email:
            raise ValueError('The given email must be set')

        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=True,
                          is_staff=False, is_superuser=False,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff superuser
        """

        u = self.create_user(email, password, **extra_fields)
        # Could just pass these as extra_fields to create_user()
        # but this is more explicit and allows create_user to ensure
        # that the correct settings are enforced for a normal user.
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u
