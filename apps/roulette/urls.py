#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^$', direct_to_template,
           {'template': 'roulette/index.html'},
           name='roulette'),
    
    )
