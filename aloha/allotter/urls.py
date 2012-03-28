from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('allotter.views',
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^(?P<reg_no>\d+)/apply/$', 'apply'),
    url(r'^(?P<reg_no>\d+)/details/$', 'submit_details'),
    url(r'^(?P<reg_no>\d+)/get_pdf/$', 'generate_pdf'),
    url(r'^(?P<reg_no>\d+)/submit/$', 'submit_options', name='submit_options'),
    url(r'^(?P<reg_no>\d+)/complete/$', 'complete_allotment', name='complete_allotment'),
    url(r'^$', 'user_login'), 
)
