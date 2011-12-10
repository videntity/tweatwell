#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.contrib.auth import login, authenticate
from httpauth import HttpBasicAuthentication
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime

def authorize(request):
    a=HttpBasicAuthentication()
    if a.is_authenticated(request):
        login(request,request.user)
        auth=True
    else:
        if request.user.is_authenticated():
            auth=True
        else:
            auth=False
    return auth



