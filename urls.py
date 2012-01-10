from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tweatwell.apps.checkin.views import checkin
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
    
    #application specific urls -------------------------------------------------
    url(r'^$', checkin, name="checkin"),
    url(r'^checkin/',       include('tweatwell.apps.checkin.urls')),
    url(r'^roulette/',      include('tweatwell.apps.roulette.urls')),
    url(r'^recipes/',       include('tweatwell.apps.recipes.urls')),
    url(r'^tips/',          include('tweatwell.apps.tips.urls')),
    url(r'^quiz/',          include('tweatwell.apps.quiz.urls')),
    url(r'^questions/',     include('tweatwell.apps.questions.urls')),
    url(r'^profile/',       include('tweatwell.apps.profile.urls')),
    url(r'^leaderboard/',   include('tweatwell.apps.leaderboard.urls')),
    #Twitter searchbot
    url(r'^twitsearchbot/(?P<cron_key>[^/]+)/$', executetwitsearchbot, name="executetwitsearchbot"),
    

    # enable the admin interface:
    (r'^admin/', include(admin.site.urls)),
    
    
    
)





