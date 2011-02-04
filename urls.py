from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tweatwell.accounts.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from tweatwell.web.views import *
from tweatwell.web.stats.views import *
from tweatwell.web.rawdata.views import *
from tweatwell.web.upload.views import *
from tweatwell.web.mybox.views import *
from tweatwell.web.twitbot.views import *
from tweatwell.web.pointsrank.views import *
from tweatwell.web.coachespoll.views import *
from tweatwell.web.profile.views import *
from tweatwell.accounts.views import *
from settings import BASE_DIR
from django.contrib.auth.views import login, logout, logout_then_login, password_change
from django.contrib.auth.forms import AuthenticationForm
#from registration.backends.default import DefaultBackend
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



urlpatterns = patterns('',
    #serve static content		
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': STATIC_ROOT}),


    ##login urls ---------------------------------------------------------------
    url(r'^login/', login, { 'template_name': 'registration/login.html' }),
    url(r'^logout/', logout_then_login),

    ##account urls -------------------------------------------------------------
    
    url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationForm}, name="request_account"),

    (r'^avatar/', include('avatar.urls')),
    
    url(r'^faq/$', direct_to_template,
           {'template': 'faq.html'},
           name='faq.html'),

    url(r'^tos/$', direct_to_template,
           {'template': 'tos.html'},
           name='tos'),
    
    url(r'^privacy/$', direct_to_template,
           {'template': 'privacy.html'},
           name='privacy'),



    url(r'^accounts/profile/$', 'tweatwell.accounts.views.account_settings', name="account_settings"),
    url(r'^accounts/register/complete/$', direct_to_template,
           {'template': 'registration/registration_complete.html'},
           name='registration_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        'registration.views.activate',
        {'extra_context': {'auth_form': AuthenticationForm()}},
        name='registration_activate'),
    

    url(r'^accounts/', include('django.contrib.auth.urls')),
    
    #application specific urls -------------------------------------------------
    url(r'^$', home_index, name="home_index"),
    url(r'^download/$', 'django.views.generic.simple.direct_to_template', {'template': 'download/index.html'}, name="download"),
    url(r'^upload/$', 'django.views.generic.simple.direct_to_template', {'template': 'upload/index.html'}, name="upload"),
    url(r'^transmit/$', 'django.views.generic.simple.direct_to_template', {'template': 'transmit/index.html'}, name="transmist"),
    url(r'^stats/$', 'django.views.generic.simple.direct_to_template', {'template': 'stats/index.html'}, name="stats"),
    url(r'^rawdata/$', 'django.views.generic.simple.direct_to_template', {'template': 'rawdata/index.html'}, name="raw"),


    url(r'^tt/$', 'django.views.generic.simple.direct_to_template', {'template': 'testtemplate.html'}, name="testtemplate"),
    url(r'^rankings/$', 'django.views.generic.simple.direct_to_template', {'template': 'rankings/index.html'}, name="rankings"),
    url(r'^rankings/coaches/$', coaches, name="coaches"),
    url(r'^rankings/points/$', points, name="points"),

    #stats
    url(r'^stats/wt/(?P<user>\w+)/$', stats_wt, name="stats_wt"),
    
    #mybox
    url(r'^mybox/(?P<user>\w+)/$', mybox, name="mybox"),
    
    #rawdata
    url(r'^rawdata/bp/(?P<user>\w+)/$', rawdata_bp, name="rawdata_bp"),
    url(r'^rawdata/wt/(?P<user>\w+)/$', rawdata_wt, name="rawdata_wt"),
    url(r'^rawdata/spd/(?P<user>\w+)/$', rawdata_spd, name="rawdata_spd"),
    url(r'^rawdata/all/(?P<user>\w+)/$', rawdata_all, name="rawdata_all"),
    
    #Upload
    url(r'^ajaxupload/wt/(?P<user>\w+)/$', upload_wt_ajax, name="upload_wt_ajax"),
    url(r'^ajaxupload/ci/(?P<user>\w+)/$', upload_ci_ajax, name="upload_ci_ajax"),
    
    url(r'^tupload/(?P<omheprefix>\w+)/(?P<user>\w+)/$', upload_texti, name="upload_texti"),
    url(r'^upload/ci/(?P<user>\w+)/$', upload_ci, name="upload_ci"),
    url(r'^ajaxupload/omhe/(?P<user>\w+)/$', upload_omhe_ajax, name="upload_omhe_ajax"),
    url(r'^upload/omhe/(?P<user>\w+)/$', upload_omhe, name="upload_omhe"),
    
    url(r'^upload/comment/(?P<user>\w+)/$', upload_comment, name="upload_comment"),

    url(r'^upload/error/(?P<code>\w+)/$', upload_error, name="upload_error"),

    #User public profiles
    url(r'^profiles/$', profiles, name="profiles"),
    url(r'^profile/(?P<user>\w+)/$', user_profile, name="user_profile"),
    url(r'^userprofile/(?P<user>\w+)/$', user_profile, name="user_profile"),
    url(r'^coachesprofiles/$', coaches_profile_list, name="coaches_profile_list"),

    
    #Twitter searchbot
    url(r'^executetwitsearchbot/', executetwitsearchbot, name="executetwitsearchbot"),
    url(r'^buildpointsrank/', buildpointsrank, name="buildpointsrank"),
    
     #Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
     #to INSTALLED_APPS to enable admin documentation:
     #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # enable the admin interface:
    (r'^admin/', include(admin.site.urls)),
    
    
    
)





