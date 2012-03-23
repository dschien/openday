from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.views.generic import ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from openday.models import Survey
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'openday.views.start'),
     url(r'^start', 'openday.views.start'),
#     url(r'^gender', 'openday.quest.views.gender'),
     url(r'^gender', 'openday.views.gender'),
     url(r'^climate', 'openday.views.climate'),
     url(r'^rank', 'openday.views.rank'),
     url(r'^rate', 'openday.views.rate'),
     url(r'^app', 'openday.views.app'),
     url(r'^branch', 'openday.views.branch'),     
     url(r'^thankyou', 'openday.views.thankyou'),
    
     url(r'^about', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^contact', 'openday.views.contact'),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     #(r'^favicon\.ico$', redirect_to, {'url': '/media/favicon.ico'}),
     (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
     (r'^favicon\.ico$', redirect_to, {'url': ' {{ STATIC_URL }}favicon.ico'}),
     url(r'^list', ListView.as_view(
            queryset=Survey.objects.order_by('-survey_date')[:50],
            context_object_name='past_surveys_list',
            template_name='list.html')),
)