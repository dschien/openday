from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'openday.views.start'),
     url(r'^start', 'openday.views.start'),
#     url(r'^gender', 'openday.quest.views.gender'),
     url(r'^gender', 'openday.views.gender2'),
     url(r'^climate', 'openday.views.climate'),
     url(r'^app', 'openday.views.app'),
     url(r'^review', 'openday.views.review'),
     url(r'^finish', 'openday.views.finish'),
     
     
#     url(r'^app', redirect_to, {'url': 'http://sympact.cs.bris.ac.uk/openday/godee/'}),
     url(r'^about', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^contact', 'openday.views.contact'),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     #(r'^favicon\.ico$', redirect_to, {'url': '/media/favicon.ico'}),
     (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
     (r'^favicon\.ico$', redirect_to, {'url': ' {{ STATIC_URL }}favicon.ico'}),
)
