from django.conf.urls import patterns, url, include
from . import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'beer', api.BeerViewSet)

urlpatterns = patterns('api',
                       url(r'^', include(router.urls)),
                       )
