from django.forms import widgets
from rest_framework import serializers

from .models import User

class AllDataUserSerializer(serializers.ModelSerializer):
    """
    Returns all details.  Intended for a user to view or edit their own profile, etc.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_joined', 'first_name', 'last_name', 'show_name_on_sightings')
