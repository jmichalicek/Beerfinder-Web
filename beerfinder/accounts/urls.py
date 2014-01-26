from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
                       url(r'^my_profile/$', 'edit_profile', name='accounts_edit_profile'),
)
