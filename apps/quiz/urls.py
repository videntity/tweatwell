from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import auth
from views import *



urlpatterns = patterns('',
    url(r'incomplete/$', 'django.views.generic.simple.direct_to_template', {'template': 'quiz/incomplete.html'}, name="incomplete"),
    url(r'category/(?P<category>[^/]+)/complete/$', complete, name="quiz_complete"),
    url(r'^category/(?P<category>[^/]+)/$', take_quiz, name="take_quiz"),
    url(r'^dashboard/$', dashboard, name="dashboard"),  
    )