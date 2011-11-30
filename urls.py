from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tweatwell.web.home.views import *
from tweatwell.web.stats.views import *
from tweatwell.web.rawdata.views import *
from tweatwell.web.upload.views import *
from tweatwell.web.mybox.views import *
from tweatwell.web.twitbot.views import *
from tweatwell.web.pointsrank.views import *
from tweatwell.web.coachespoll.views import *
from tweatwell.web.profile.views import *
from tweatwell.web.accounts.views import *
from django.contrib.auth.views import login, logout, logout_then_login, password_change

#from registration.backends.default import DefaultBackend
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # login urls ---------------------------------------------------------------
    (r'^janrain/', include('tweatwell.web.janrain.urls')),
    # account urls -------------------------------------------------------------
    url(r'^accounts/', include('tweatwell.web.accounts.urls')),  

    (r'^avatar/', include('avatar.urls')),
    
    url(r'^faq/$', direct_to_template,
           {'template': 'faq.html'},
           name='faq'),

    url(r'^tos/$', direct_to_template,
           {'template': 'tos.html'},
           name='tos'),
    
    url(r'^privacy/$', direct_to_template,
           {'template': 'privacy.html'},
           name='privacy'),

    
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





