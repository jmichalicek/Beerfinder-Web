from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sightings', api.SightingViewSet)

urlpatterns = patterns('api',
                       url(r'^', include(router.urls)),
                       )
