#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'^$', profile, name='profile'),
    
    url(r'^download$', download_xls, name='download_xls'),
    
    url(r'admin-profile/(?P<username>[^/]+)/$', admin_profile,
        name='admin_profile'),

    )