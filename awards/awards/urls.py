from django.conf.urls.defaults import patterns, include, url

from awards.sigplan.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    
    (r'^nominate/', nominate),
    
    # Examples:
    # url(r'^$', 'awards.sigplan.views.home', name='home'),
    # url(r'^awards/', include('awards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    
    
)
