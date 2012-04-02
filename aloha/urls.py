from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^allotter/', include('allotter.urls')),
	url(r'^browser-version', direct_to_template, {'template': 'browser-version.html'}),
	url(r'^about', direct_to_template, {'template': 'about.html'}),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    # Examples:
    # url(r'^$', 'aloha.views.home', name='home'),
    # url(r'^aloha/', include('aloha.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
