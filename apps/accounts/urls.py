#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'login/', simple_login,  name='simple_login'),
    url(r'logout/', mylogout, name='mylogout'),
    url(r'password-reset-request/', password_reset_request,
        name='password_reset_request'),     
    url(r'signup/', signup, name='signup'),
    url(r'change-password/', 'django.contrib.auth.views.password_change',
        name="password_change"),
    url(r'profile/', account_settings, name='account_settings'),
    url(r'reset-password/(?P<reset_password_key>[^/]+)/$', reset_password,
        name='password_reset_request'),

    url(r'signup-verify/(?P<signup_key>[^/]+)/$', signup_verify,
        name='signup_verify'),
    
    )