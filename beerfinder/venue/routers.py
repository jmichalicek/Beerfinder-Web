from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'venues', api.VenueViewSet)
router.register(r'foursquare_venues', api.FoursquareVenueViewSet, base_name='foursquare_venues')

search_venues = api.FoursquareVenueViewSet.as_view({'get': 'search'})


urlpatterns = patterns('api',
                       url(r'foursquare_venues/search/$', search_venues, name='search_foursquare_venues'),
                       url(r'^', include(router.urls)),
                       )
