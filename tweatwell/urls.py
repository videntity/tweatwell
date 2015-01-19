
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from apps.checkin.views import checkin
from apps.twitbot.views import *

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',


    # account & login urls -----------------------------------------------------
     url(r'^accounts/', include('apps.accounts.urls')),   
    
    # Media and Static -  comment out for production config! -------------
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}),
    
    #
    (r'^avatar/', include('avatar.urls')),
    #
    url(r'^faq/$',TemplateView.as_view(template_name='static_page/faq.html'), name='faq'),
    url(r'^tos/$',TemplateView.as_view(template_name='static_page/tos.html'), name='tos'),    
    url(r'^privacy/$',TemplateView.as_view(template_name='static_page/privacy.html'), name='privacy'),    
    #    
        
    #    
    #    direct_to_template,
    #       {'template': 'static_page/faq.html'},
    #       name='faq'),
    #
    #url(r'^tos/$', direct_to_template,
    #       {'template': 'static_page/tos.html'},
    #       name='tos'),
    #
    #url(r'^privacy/$', direct_to_template,
    #       {'template': 'static_page/privacy.html'},
    #       name='privacy'),
    
    #application specific urls -------------------------------------------------
    url(r'^$', checkin, name="checkin"),
    url(r'^checkin/',       include('apps.checkin.urls')),
    url(r'^roulette/',      include('apps.roulette.urls')),
    url(r'^recipes/',       include('apps.recipes.urls')),
    url(r'^tips/',          include('apps.tips.urls')),
    url(r'^quiz/',          include('apps.quiz.urls')),
    url(r'^questions/',     include('apps.questions.urls')),
    url(r'^profile/',       include('apps.profile.urls')),
    url(r'^leaderboard/',   include('apps.leaderboard.urls')),
    #Twitter searchbot
    url(r'^twitsearchbot/(?P<cron_key>[^/]+)/$', executetwitsearchbot, name="executetwitsearchbot"),
    

    # enable the admin interface:
    (r'^admin/', include(admin.site.urls)),
    
    
    
)





