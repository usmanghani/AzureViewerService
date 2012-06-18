from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hilal.views.home', name='home'),
    # url(r'^hilal/', include('hilal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^hilal/$', 'hilal.views.hilal_index', name='hilal_index'),
    url(r'^hilal/(?P<month>\w+)/$', 'hilal.views.hilal', name='hilal'),
    url(r'^pray/(?P<year>\d{2,4})/(?P<location>\w+)/$', 'hilal.views.pray_year', name='pray_year'),
    url(r'^pray/(?P<year>\d{2,4})/(?P<month>\d{1,2})/(?P<location>\w+)/$', 'hilal.views.pray_month', name='pray_month'),
    url(r'^pray/(?P<year>\d{2,4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<location>\w+)/$', 'hilal.views.pray_date', name='pray_date'),
    url(r'^pray/(?P<location>\w+)/$', 'hilal.views.pray', name='pray'),
)
