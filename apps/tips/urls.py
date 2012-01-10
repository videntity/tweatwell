#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'^rotate/(?P<cron_key>[^/]+)/$', rotate_tip, name='rotate_tip'),
    
    )
