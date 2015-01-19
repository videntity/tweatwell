#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    
    url(r'^$', recipe,
        name='recipe'),
    
    url(r'comment/(?P<recipe_id>[^/]+)/$', recipe_comment,
        name='recipe_comment'),

    )