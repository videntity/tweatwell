#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'^$', leaderboard, name='leaderboard'),
    url(r'^score$', score, name='score'),
    
    )