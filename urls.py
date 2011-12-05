from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tweatwell.apps.home.views import *
from tweatwell.apps.stats.views import *
from tweatwell.apps.upload.views import *
from tweatwell.apps.twitbot.views import *
from tweatwell.apps.pointsrank.views import *
from tweatwell.apps.coachespoll.views import *

#from registration.backends.default import DefaultBackend
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # login urls ---------------------------------------------------------------
    #(r'^janrain/', include('tweatwell.apps.janrain.urls')),
    # account urls -------------------------------------------------------------
    
     # Media and Static -  comment out for production config! -------------
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}),
    
    url(r'^accounts/', include('tweatwell.apps.accounts.urls')),  

    (r'^avatar/', include('avatar.urls')),
    
    url(r'^faq/$', direct_to_template,
           {'template': 'static_page/faq.html'},
           name='faq'),

    url(r'^tos/$', direct_to_template,
           {'template': 'static_page/tos.html'},
           name='tos'),
    
    url(r'^privacy/$', direct_to_template,
           {'template': 'static_page/privacy.html'},
           name='privacy'),

    
    #application specific urls -------------------------------------------------
    url(r'^$', home, name="home"),
    
    url(r'^download/$', 'django.views.generic.simple.direct_to_template', {'template': 'download/index.html'}, name="download"),
    url(r'^upload/$', 'django.views.generic.simple.direct_to_template', {'template': 'upload/index.html'}, name="upload"),
    url(r'^transmit/$', 'django.views.generic.simple.direct_to_template', {'template': 'transmit/index.html'}, name="transmist"),
    
    url(r'^tt/$', 'django.views.generic.simple.direct_to_template', {'template': 'testtemplate.html'}, name="testtemplate"),
    url(r'^rankings/$', 'django.views.generic.simple.direct_to_template', {'template': 'rankings/index.html'}, name="rankings"),
    url(r'^rankings/coaches/$', coaches, name="coaches"),
    url(r'^rankings/points/$', points, name="points"),
    
    
    #Upload
    url(r'^ajaxupload/wt/(?P<user>\w+)/$', upload_wt_ajax, name="upload_wt_ajax"),
    url(r'^ajaxupload/ci/(?P<user>\w+)/$', upload_ci_ajax, name="upload_ci_ajax"),
    
    url(r'^tupload/(?P<omheprefix>\w+)/(?P<user>\w+)/$', upload_texti, name="upload_texti"),
    url(r'^upload/ci/(?P<user>\w+)/$', upload_ci, name="upload_ci"),
    url(r'^ajaxupload/omhe/(?P<user>\w+)/$', upload_omhe_ajax, name="upload_omhe_ajax"),
    url(r'^upload/omhe/(?P<user>\w+)/$', upload_omhe, name="upload_omhe"),
    url(r'^upload/comment/(?P<user>\w+)/$', upload_comment, name="upload_comment"),
    url(r'^upload/error/(?P<code>\w+)/$', upload_error, name="upload_error"),


    
    #Twitter searchbot
    url(r'^executetwitsearchbot/', executetwitsearchbot, name="executetwitsearchbot"),
    url(r'^buildpointsrank/', buildpointsrank, name="buildpointsrank"),
    

    # enable the admin interface:
    (r'^admin/', include(admin.site.urls)),
    
    
    
)





