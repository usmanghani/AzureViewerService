from django.conf.urls import patterns, include, url
from AzureViewerService.views import *
import django.contrib.admindocs
import django.contrib.admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^hello/$', 'AzureViewerService.views.hello', name='hello'),
    url(r'^time/$', 'AzureViewerService.views.current_datetime', name='time'),
    url(r'^kick/$', 'AzureViewerService.views.kick', name='kick'),
    url(r'^time/plus/(\d{1,2})/$', 'AzureViewerService.views.hours_ahead', name='hours_ahead'),
    # Examples:
    url(r'^$', 'AzureViewerService.views.home', name='home'),
    # url(r'^AzureViewerService/', include('AzureViewerService.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
