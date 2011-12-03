#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.contrib.auth import login, authenticate
from httpauth import HttpBasicAuthentication
from django.http import HttpResponse
from models import Permission, ValidSignupKey
from django.contrib.auth.models import User
from datetime import datetime

def validate_signup(signup_key):
    try:
        vc=ValidSignupKey.objects.get(signup_key=signup_key)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False   
    except(ValidSignupKey.DoesNotExist):
        return False  
    u=vc.user
    u.is_active=True
    u.save()
    vc.delete()
    return True


def user_permissions(request):
    try:
        p=Permission.objects.filter(user=request.user)
        pl=[]
        for i in p:
            pl.append(i.permission_name)
        return tuple(pl)
    except(Permission.DoesNotExist):
        return ()
        



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



