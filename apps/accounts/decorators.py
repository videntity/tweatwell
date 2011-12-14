#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


"""
    Decorator to check for credentials before responding on json requests.
"""

from functools import update_wrapper, wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from utils import authorize, user_permissions




def access_required(permission):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if permission in user_permissions(request):
                    return func(request, *args, **kwargs)
            else:
                    return HttpResponse("Permission Denied.  Your account credentials \
                            are valid but you do not have the permission \
                            required to access this function.", status=401)
        return wraps(func)(inner_decorator)

    return decorator
    

