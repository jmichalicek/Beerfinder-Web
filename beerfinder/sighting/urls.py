from django.conf.urls import patterns, include, url

urlpatterns = patterns('sighting.views',
                       url(r'nearby/', 'sightings_near_user', name='sightings_near_user'),
                       url(r'add_sighting/', 'add_sighting', name='add_sighting'),
                       url(r'(?P<sighting_id>\d+)/$', 'sighting_detail', name='sighting_detail'),
)
