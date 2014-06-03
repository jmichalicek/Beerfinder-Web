from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

from allauth.account.forms import ChangePasswordForm

from .models import User
from .serializers import AllDataUserSerializer

class UserProfileApiView(APIView):
    """
    API Views for a user to view and edit their own profile.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        """
        Return the profile for the current user
        """
        serialized = AllDataUserSerializer(request.user)
        return Response(serialized.data)

    def post(self, request):
        """
        Update the profile for the current user
        """

        serializer = AllDataUserSerializer(request.user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApiView(APIView):
    """
    Allow a user to change their password
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
