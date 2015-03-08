from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sightings', api.SightingViewSet)
router.register(r'sighting_images', api.SightingImageViewSet)
router.register(r'sighting_comments', api.SightingCommentViewSet, base_name='sighting_comment')

nearby_sightings = api.NearbySightingAPIView.as_view() #api.SightingViewSet.as_view({'get': 'get_nearby_sightings'})

urlpatterns = patterns('api',
                       url(r'nearby_sightings/$', nearby_sightings, name='nearby_sighting-list'),
                       url(r'^sighting_confirmations/$', api.SightingConfirmationAPIView.as_view(),
                           name='sighting_confirmation-list'),
                       url(r'^', include(router.urls)),
                       )
