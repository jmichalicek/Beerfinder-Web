from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
profile_detail = api.UserProfileApiView.as_view()
change_password = api.ChangePasswordApiView.as_view()

urlpatterns = patterns('api',
                       url(r'profile/me/', profile_detail),
                       url(r'profile/change_password', change_password),
                       url(r'^', include(router.urls)),
                       )
