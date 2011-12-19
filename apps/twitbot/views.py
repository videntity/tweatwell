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

from operator import itemgetter, attrgetter
import json, sys, StringIO, pycurl
from omhe.core.parseomhe import parseomhe

def executetwitsearchbot(request):
    #get the most recent since_id from db
    tb=TwitBot.objects.get(pk=1)
    
    d=twitbotsearch(settings.TWITTERHASH, tb.since_id)    
    
    for i in d['results']:
        jsonstr=json.dumps(i, indent = 4,)
        x=dict(json.loads(jsonstr))
        #if the from_user is in our DB, then create a Freggie 
        if  int(tb.since_id) <= int(x['id']):
            try:
                up=UserProfile.objects.get(twitter=x['from_user'])
                print "process"
                print x['created_at']
                print convert_twitter_date(str(x['created_at']))
            
            except(UserProfile.DoesNotExist):
                pass
            except:
                print str(sys.exc_info())
                pass
                #return HttpResponse(str(sys.exc_info()), status=500)
        #tb.since_id=x['id']
        #tb.save()
        
    return HttpResponse("OK")
    
def buildpointsrank(request):
    """Build points rankk"""
    usr=UserStatusReport.objects.all().delete()
    
    
    #"read from restcat"
    URL="%sapi/population/omhe/all/" % (settings.RESTCAT_SERVER)
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
    json_string= b.getvalue()
    l=list(json.loads(json_string))
    sl=sorted(l, key=itemgetter('subj'))
    ul=User.objects.all()
    ranklist=[]
    rankdict={}
    for i in ul:
        points=0
        rankdict['points']=0
        rankdict['alc']=0
        rankdict['wtr']=0
        rankdict['frt']=0
        rankdict['veg']=0
        rankdict['crb']=0
        rankdict['pro']=0
        rankdict['dry']=0
        rankdict['ans']=0
        rankdict['user']=i
        rankdict['username']=i.username
        rankdict['email']=i.email
        for j in l:

            if j.has_key('omhe') and j.has_key('texti') and str(j['subj'])==str(i.email):    
                #print j
                UserStatusReport.objects.create(user=i, status=j['texti'])

            if j.has_key('points') and str(j['subj'])==str(i.email):
                points=int(points) + int(j['points'])
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="alc":
                    rankdict['alc']=rankdict['alc']+1
            
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="wtr":
                    rankdict['wtr']=rankdict['wtr']+1
            
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="frt":
                    rankdict['frt']=rankdict['frt']+1
                
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="veg":
                    rankdict['veg']=rankdict['veg']+1
                
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="crb":
                    rankdict['crb']=rankdict['crb']+1
                
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="pro":
                    rankdict['pro']=rankdict['pro']+1
            
            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="dry":
                    rankdict['dry']=rankdict['dry']+1

            if j.has_key('omhe') and str(j['subj'])==str(i.email):
                if j['omhe']=="ans":
                    rankdict['ans']=rankdict['ans']+1
        
        rankdict['points']=points
        ranklist.append(rankdict)
        rankdict={}
        
    newranksort = sorted(ranklist, key=itemgetter('points'), reverse=True)
    rank=0
    all=PointsRank.objects.all().delete()
    fr=FoodReport.objects.all().delete()
    for i in newranksort:
        rank+=1
        
        u=User.objects.get(username=i['user'])
        try:
            up=u.get_profile()

            try:
                pr=PointsRank.objects.get(user=i['user'])
                pr.rank=rank
                pr.save()
                
                
            except(PointsRank.DoesNotExist):
                pr=PointsRank.objects.create(user=i['user'],
                                             rank=rank, points=i['points'])
                pr.save()
                #print sys.exc_info()
                
            
            fr=FoodReport.objects.create(
                            user=i['user'],
                            points=i['points'],
                            alcohol=i['alc'],
                            fruits=i['frt'],
                            veggies=i['veg'],
                            water=i['wtr'],
                            answers=i['ans'],)
            fr.save()    
            
            
        except(UserProfile.DoesNotExist):
            pass
        
    #build a report to send to judges
    fr=FoodReport.objects.all()
    r="user|points|alcohol|fruits|veggies|water|answers\n"
    for f in fr:
        l="%s|%s|%s|%s|%s|%s|%s\n" % (f.user, f.points, f.alcohol, f.fruits,
                                      f.veggies, f.water, f.answers)
        r="%s%s" %(r,l)
    #print r
    
    
    try:
        up=UserProfile.objects.filter(coach=True)
    
        el=[]
        for u in up:
            el.append(u.user.email)
        from django.core.mail import send_mail
        send_mail("Tweatwell Report", r, settings.EMAIL_HOST_USER, el)
    except(UserProfile.DoesNotExist):
        pass
    return HttpResponse("OK")