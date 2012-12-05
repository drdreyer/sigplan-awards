from django.conf.urls.defaults import patterns, include, url

from awards.sigplan.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    
    (r'^nominate/', nominate),
    (r'^edit_award/(?P<award_id>\w+)/$', edit_award),
    (r'^add_committee_member/(?P<award_id>\w+)/$', add_committee_member),
    (r'^award_member/(?P<award_id>\w+)/$', award_member),
    (r'^activate_committee_member/(?P<web_key>\w+)/$', activate_committee_member),
    (r'^make_czar/(?P<award_id>\w+)/(?P<member_id>\w+)/', make_czar),
    (r'^thank_nominator/$', thank_nominator),
    (r'^complete_nomination/(?P<web_key>\w+)/$', complete_nomination),
    (r'^candidate/(?P<candidate_id>\w+)/$', candidate),
    (r'^email_supporter/(?P<supporter_id>\w+)/$', email_supporter),
    (r'^email_supporters/(?P<candidate_id>\w+)/$', email_supporters),
    (r'^support_letter/(?P<web_key>\w+)/$', support_letter),
    
    (r'^accounts/authentication/$', sigplan_authenticate),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    (r'^accounts/profile/', profile),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/passwordd_reset_form.html'}),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'registration/passwordd_reset_done.html'}),
    (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'registration/passwordd_reset_confirm.html'}),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'registration/passwordd_reset_complete.html'}),
    
    # Examples:
    # url(r'^$', 'awards.sigplan.views.home', name='home'),
    # url(r'^awards/', include('awards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    
    
)
