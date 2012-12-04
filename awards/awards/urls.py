from django.conf.urls.defaults import patterns, include, url

from awards.sigplan.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    
    (r'^nominate/', nominate),
    (r'^czar/', czar),
#    (r'^accounts/login/', account_login),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
#    (r'^accounts/logout/', account_logout),
    (r'^accounts/authentication/$', sigplan_authenticate),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    (r'^accounts/profile/', profile),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/passwordd_reset_form.html'}),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    
    # Examples:
    # url(r'^$', 'awards.sigplan.views.home', name='home'),
    # url(r'^awards/', include('awards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    
    
)
