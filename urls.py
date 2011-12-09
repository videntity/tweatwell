from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tweatwell.apps.checkin.views import *
from tweatwell.apps.stats.views import *
from tweatwell.apps.twitbot.views import *

#from registration.backends.default import DefaultBackend
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    # account & login urls -----------------------------------------------------
     url(r'^accounts/', include('tweatwell.apps.accounts.urls')),   
    
    # Media and Static -  comment out for production config! -------------
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}),
    

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

    #TODO: this is temp for skinning
    url(r'^roulette/$', direct_to_template,
           {'template': 'roulette/index.html'},
           name='roulette'),

    
    #application specific urls -------------------------------------------------
    url(r'^$', checkin, name="checkin"),
    
    #Twitter searchbot
    url(r'^executetwitsearchbot/', executetwitsearchbot, name="executetwitsearchbot"),
    url(r'^buildpointsrank/', buildpointsrank, name="buildpointsrank"),
    

    # enable the admin interface:
    (r'^admin/', include(admin.site.urls)),
    
    
    
)





