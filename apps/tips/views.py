#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import CurrentTip
from datetime import date, timedelta



def rotate_tip(request, cron_key):
    
    if cron_key != settings.CRON_KEY:
        return HttpResponse("Forbidden", status=401)
    ct= CurrentTip.objects.get(pk=1)
    ct.index=ct.index+1
    ct.save()
    return HttpResponse("Tip rotated")
    
    
    