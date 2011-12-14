#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$',              roulette_home,  name='roulette_home'),
    url(r'spin-results/$',  spin_results,   name='spin_results'),
    )
