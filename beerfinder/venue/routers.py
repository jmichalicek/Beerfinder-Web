from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'venues', api.VenueViewSet)
router.register(r'foursquare_venues', api.FoursquareVenueViewSet, base_name='foursquare_venues')

urlpatterns = patterns('api',
                       url(r'^', include(router.urls)),
                       )
