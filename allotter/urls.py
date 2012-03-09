from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
	url(r'^$', 'hello'),
    url(r'^login/$', 'user_login'),
    url(r'^register/$', 'user_register'),
    url(r'^apply/$', 'apply'),
	url(r'^quit/$', 'quit'),
	url(r'^save/$', 'save'),
)
