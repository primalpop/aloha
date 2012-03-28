from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^allotter/', include('allotter.urls')),
    # Examples:
    # url(r'^$', 'aloha.views.home', name='home'),
    # url(r'^aloha/', include('aloha.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)