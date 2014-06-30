from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sightings', api.SightingViewSet)

nearby_sightings = api.NearbySightingAPIView.as_view() #api.SightingViewSet.as_view({'get': 'get_nearby_sightings'})

urlpatterns = patterns('api',
                       url(r'sightings/nearby/', nearby_sightings),
                       url(r'^', include(router.urls)),
                       )
