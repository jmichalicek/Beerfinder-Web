from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(_('email address'), max_length=100, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    username = models.CharField(max_length=50, blank=True, help_text=_('Username to alternately display instead of email address'), unique=True)
    show_name_on_sightings = models.BooleanField(default=True, blank=True)

    objects = UserManager()

    def __unicode__(self):
        return u'{0}'.format(self.email)

    def get_short_name(self):
        return u'{0}'.format(self.first_name)

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        super(User, self).save(*args, **kwargs)
