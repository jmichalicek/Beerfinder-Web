from django.conf.urls import patterns, include, url

urlpatterns = patterns('beer.views',
                       url(r'^add/', 'add_beer', name='add_beer'),
                       url(r'^(?P<beer_slug>[-\w_]+)/', 'beer_detail', name='beer_detail'),
                       url(r'^$', 'list_beer', name='show_beer_list'),
)
