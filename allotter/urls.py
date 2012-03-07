from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
	url(r'^$', 'index'),
    url(r'^login/$', 'user_login'),
    url(r'^register/$', 'user_register'),
	url(r'^hello/$', 'hello'),
    url(r'^apply/$', 'apply'),
)
