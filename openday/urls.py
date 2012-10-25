from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.views.generic import ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from openday.models import Survey
admin.autodiscover()

from django.contrib import databrowse
from openday.models import Survey, Selection 

databrowse.site.register(Survey)
databrowse.site.register(Selection)

from openday import views

urlpatterns = patterns('',                       
     url(r'^(?P<group>\w+)/start', views.start),
#     url(r'$', redirect_to, {'url': '/openday/test/start'}), 
#     url(r'^gender', 'openday.quest.views.gender'),
     url(r'^(?P<group>\w+)/gender', views.gender),
     url(r'^(?P<group>\w+)/climate', views.climate),
     url(r'^(?P<group>\w+)/rank', views.rank),
     url(r'^(?P<group>\w+)/rate', views.rate),
     url(r'^(?P<group>\w+)/app', views.app),
     url(r'^(?P<group>\w+)/prereview', views.prereview),
     url(r'^(?P<group>\w+)/review', views.review),     
     url(r'^(?P<group>\w+)/thankyou', views.thankyou),
     url(r'export', views.export),
    
     url(r'about', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'contact', 'openday.views.contact'),
    # Uncomment the next line to enable the admin:
     url(r'admin/', include(admin.site.urls)),
     #(r'^favicon\.ico$', redirect_to, {'url': '/media/favicon.ico'}),
     (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
     (r'^favicon\.ico$', redirect_to, {'url': ' {{ STATIC_URL }}favicon.ico'}),
     url(r'^list', ListView.as_view(
            queryset=Survey.objects.order_by('-survey_date')[:50],
            context_object_name='past_surveys_list',
            template_name='list.html')),
    (r'^databrowse/(.*)', databrowse.site.root),
    url(r'^(?P<group>\w+$)', views.redirection_view),
    url(r'^$', views.redirection_view,  {'group': 'main'}),
)