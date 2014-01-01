from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'beerfinder.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'api/', include('beer.routers')),
                       url(r'api/', include('sighting.routers')),
                       url(r'accounts/', include('django.contrib.auth.urls')),
                       url(r'sightings/', include('sighting.urls')),

)
