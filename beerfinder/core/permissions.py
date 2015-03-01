from __future__ import unicode_literals

"""
Django Rest Framework custom permissions
"""

from rest_framework import permissions

# what about for querysets?
class IsOwnerOrReadOnlyPermissions(permissions.IsAuthenticatedOrReadOnly):
    """
    Object-level permission for Django Rest Framework to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):

        model_cls = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_cls is None and queryset is not None:
            model_cls = queryset.model

        assert model_cls, ('Cannot apply IsOwnerPermissions on a view that'
                           ' does not have `.model` or `.queryset` property.')

        # Instance must have an attribute named `owner`.
        return (request.method in permissions.SAFE_METHODS
                or (request.user and request.user.is_authenticated()
                and obj.user == request.user))
