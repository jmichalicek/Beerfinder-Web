from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'beerfinder.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'api/', include('beer.routers')),
                       url(r'api/', include('sighting.routers')),
                       url(r'api/', include('venue.routers')),
                       url(r'accounts/', include('allauth.urls')),
                       #url(r'accounts/', include('django.contrib.auth.urls')),
                       url(r'beer/', include('beer.urls')),
                       url(r'sightings/', include('sighting.urls')),
                       url(r'^$', 'sighting.views.sightings_list', name='index'),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
