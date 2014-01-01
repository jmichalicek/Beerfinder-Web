from django.conf.urls import patterns, include, url

urlpatterns = patterns('sighting.views',
                       url(r'nearby/', 'sightings_near_user', name='sightings_near_user'),
)
