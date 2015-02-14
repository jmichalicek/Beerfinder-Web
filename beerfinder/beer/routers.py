from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'beer', api.BeerViewSet, base_name='beer')
#router.register(r'serving_types', api.ServingTypeAPIView)

urlpatterns = patterns('api',
                       url(r'^serving_types/$', api.ServingTypeAPIView.as_view()),
                       url(r'^beer_styles/$', api.BeerStyleAPIView.as_view()),
                       url(r'^brewery/$', api.BreweryAPIView.as_view()),
                       url(r'^', include(router.urls)),
                       )
