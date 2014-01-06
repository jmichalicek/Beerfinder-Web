from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import User
from .serializers import AllDataUserSerializer

class UserProfileApiView(APIView):
    """
    API Views for a user to view and edit their own profile.
    """
    def get(self, request):
        """
        Return the profile for the current user
        """
        serialized = AllDataUserSerializer(request.user)
        return Response(serialized.data)
