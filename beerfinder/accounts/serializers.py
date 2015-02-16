from django.forms import widgets
from rest_framework import serializers

from .models import User

class AllDataUserSerializer(serializers.ModelSerializer):
    """
    Returns all details.  Intended for a user to view or edit their own profile, etc.
    """

    #TODO: figure out how to override the uniqueness error message for email
    class Meta:
        model = User
        lookup_field = 'id'
        fields = ('id', 'email', 'username', 'date_joined', 'first_name', 'last_name', 'show_name_on_sightings', 'send_watchlist_email')
