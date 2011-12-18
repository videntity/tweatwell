#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'comment/(?P<freggie_id>[^/]+)/$', freggie_comment,
        name='freggie_comment'),

    url(r'nonveg/$', nonveg,
        name='nonveg'),
    
    url(r'profile/$', profile,
        name='profile'),
    
    url(r'admin-profile/(?P<username>[^/]+)/$', admin_profile,
        name='admin_profile'),
    
    )