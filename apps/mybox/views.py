# Create your views here.

import sys, types
from django.http import HttpResponse, Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from tweatwell import settings
from ..utils import handle_uploaded_file
import datetime, os
import pycurl
import StringIO, json, types




@login_required
def mybox(request, user):

    email=User.objects.get(username=user)
    URL="%sapi/find/?subj=%s" % (settings.RESTCAT_SERVER, email.email)
    user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
    URL=str(URL)
    #print URL
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    json_string= b.getvalue()
    
    json_string=list(json.loads(json_string))
    #txlist=[]
    #for j in json_string:
    #    d={}
    #    d['ttype']=j['ttype']
    #    d['sndr']=j['sndr']
    #    d['rcvr']=j['rcvr']
    #    if j.has_key('texti'):
    #        d['texti']=j['texti']
    #    if j.has_key('urli'):
    #        d['urli']=j['urli']
    #    if j.has_key('idr'):
    #        d['idr']=j['idr']
    #    
    #    d['ev_dt']=j['ev_dt']
    #    d['ev_tz']=j['ev_tz']
    #    d['tx_dt']=j['tx_dt']
    #    d['tx_tz']=j['tx_tz']
    #    txlist.append(d)
        
    num_tx=len(json_string) 
    
    return render_to_response(
            'mybox/mybox.html',
            {
            'txlist':json_string,
            'num_tx': num_tx,
             },
            context_instance = RequestContext(request),)
     
     
    
    





    


