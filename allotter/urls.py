from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^apply/$', 'apply'),
    url(r'^(?P<reg_no>\w+)/submit/$', 'submit'), #change into numbers
    url(r'^(?P<reg_no>\d+)/complete/$', 'complete'), #change into numbers
    url(r'^$', 'apply'),
    #url(r'^quit/$', 'quit'),
)
