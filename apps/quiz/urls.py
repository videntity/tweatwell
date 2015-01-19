from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import *



urlpatterns = patterns('',


    url(r'incomplete/$', TemplateView.as_view(template_name='quiz/incomplete.html'), name="incomplete"),
    url(r'category/(?P<category>[^/]+)/complete/$', complete, name="quiz_complete"),
    url(r'^category/(?P<category>[^/]+)/$', take_quiz, name="take_quiz"),
    url(r'^dashboard/$', dashboard, name="dashboard"),  
    )