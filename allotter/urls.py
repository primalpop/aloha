from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
    url(r'^login/$', 'user_login'),
    #url(r'^apply/$', 'apply'),
	#url(r'^submit/$', 'submit'),
    #url(r'^quit/$', 'quit'),
)
