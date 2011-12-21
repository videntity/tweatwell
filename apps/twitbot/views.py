#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from ..accounts.models import UserProfile
from ..utils import *
from models import TwitBot
from utils import twitbotsearch, convert_twitter_date
from ..checkin.models import Freggie
from ..checkin.freggies import fruit_tuple, veg_tuple
from operator import itemgetter, attrgetter
import json, sys, StringIO, pycurl

from django.forms.models import model_to_dict

def executetwitsearchbot(request):
    freggielist=[]
    #get the most recent since_id from db
    tb=TwitBot.objects.get(pk=1)
    
    d=twitbotsearch(settings.TWITTERHASH, tb.since_id)    
    latest_since_id=tb.since_id
    
    for i in reversed(d['results']):
        jsonstr=json.dumps(i, indent = 4,)
        x=dict(json.loads(jsonstr))
        #if the from_user is in our DB, then create a Freggie 
        if  int(tb.since_id) <= int(x['id']):
            latest_since_id=x['id']
            try:
                freggie=None
                up=UserProfile.objects.get(twitter=x['from_user'])
                print "process", x['text'], x['id']
                for i in fruit_tuple:
                    if str(x['text']).lower().__contains__(i):
                        freggie = i
                for i in veg_tuple:
                    if str(x['text']).lower().__contains__(i):
                        freggie = i                        

                if freggie:
                    mydate = convert_twitter_date(str(x['created_at']))
                    f=Freggie.objects.create(user=up.user, freggie=freggie,
                                         text=x['text'], sinceid=x['id'],
                                         evdt=mydate)
                    freggiedict=model_to_dict(f, exclude=['evdt','photo',
                                                          'since_id'])
                    freggiedict['created_at']=x['created_at']
                    freggiedict['twitter_id']=x['id']
                    freggielist.append(freggiedict)
                    
            except(UserProfile.DoesNotExist):
                print "A tweat was found but no matching user profile"
            except:
                print str(sys.exc_info())
                #return HttpResponse(str(sys.exc_info()), status=500)
    tb.since_id=int(latest_since_id)+1
    tb.save()
    
    jsonstr=json.dumps(freggielist, indent = 4,)
    return HttpResponse(jsonstr,  mimetype="text/plain")
    