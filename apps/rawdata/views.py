# Create your views here.

import sys, types
from django.http import HttpResponse, Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from tweatwell import settings
import datetime
import os
import pycurl
import StringIO

@login_required
def rawdata_bp(request, user):
    email=User.objects.get(username=user)
    URL="%sapi/omhe/find/bp/%s/" % (settings.RESTCAT_SERVER, email.email)
    
    #print request.user.email
    #print URL
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=str(URL)

    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    #print b.getvalue()
    return HttpResponse(b.getvalue())
    
@login_required
def rawdata_wt(request, user):
    email=User.objects.get(username=user)
    URL="%sapi/omhe/find/wt/%s/" % (settings.RESTCAT_SERVER, email.email)
    
    #print request.user.email
    #print URL
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=str(URL)

    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    #print b.getvalue()
    return HttpResponse(b.getvalue())
    
@login_required
def rawdata_spd(request, user):
    email=User.objects.get(username=user)
    URL="%sapi/omhe/find/spd/%s/" % (settings.RESTCAT_SERVER, email.email)
    
    #print request.user.email
    #print URL
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=str(URL)

    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    #print b.getvalue()
    return HttpResponse(b.getvalue())

@login_required
def rawdata_all(request, user):
    email=User.objects.get(username=user)
    URL="%sapi/find/?subj=%s" % (settings.RESTCAT_SERVER, email.email)
    
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    #print user_and_pass
    URL=str(URL)
    #print URL
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    #print b.getvalue()
    return HttpResponse(b.getvalue())


