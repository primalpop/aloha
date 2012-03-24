from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^apply/$', 'apply'),
    url(r'^details/$', 'submit_details'),
    url(r'^get_pdf/$', 'generate_pdf'),
    url(r'^(?P<reg_no>\w+)/submit/$', 'submit_options'), #change into numbers
    url(r'^(?P<reg_no>\w+)/complete/$', 'complete'), #change into numbers
    url(r'^$', 'apply'),
    #url(r'^quit/$', 'quit'),
)
