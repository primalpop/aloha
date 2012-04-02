from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^apply/$', 'apply'),
    url(r'^details/$', 'submit_details'),
    url(r'^get_pdf/$', 'generate_pdf'),
    url(r'^submit/$', 'submit_options', name='submit_options'),
    url(r'^complete/$', 'complete_allotment', name='complete_allotment'),
    url(r'^$', 'user_login'), 
)
