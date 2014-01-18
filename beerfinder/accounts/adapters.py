"""
django-allauth login/registration adapters
"""
from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter

class RegistrationTogglableAdapter(DefaultAccountAdapter):
    """
    Allows toggling registration open/closed using settings.REGISTRATION_OPEN
    """

    def is_open_for_signup(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)
