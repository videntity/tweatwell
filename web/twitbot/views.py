# Create your views here.
from django.http import HttpResponse, Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from tweatwell.accounts.models import UserProfile
from tweatwell.web.twitbot.models import TwitBot
from tweatwell.web.twitbot.utils import twitbotsearch
from tweatwell.web.pointsrank.models import PointsRank
from tweatwell.web.upload.forms import TwitBotCIUploadForm
from tweatwell import settings
from tweatwell.web.utils import *
from django import forms
from operator import itemgetter, attrgetter
import json, sys, StringIO, pycurl

def executetwitsearchbot(request):
    #get the most recent since_id from db
    tb=TwitBot.objects.get(pk=1)
    
    d=twitbotsearch(settings.TWITTERHASH, tb.since_id)    
    for i in d['results']:
        jsonstr=json.dumps(i, indent = 4,)
        x=dict(json.loads(jsonstr))
        #if the from_user is in our DB, then create a RESTCAT transaction. 
        #print x['text'], x['from_user'], x['id']
        try:
            up=UserProfile.objects.get(twitter=x['from_user'])
            #print "process"
            #print up.user
            f=TwitBotCIUploadForm()
            f.save(up.user, x['text'])
            tb.since_id=x['id']
            tb.save()
        except(UserProfile.DoesNotExist):
            pass
        except:
            return HttpResponse(str(sys.exc_info()), status=500)
    
    return HttpResponse("OK")
    
def buildpointsrank(request):
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
        rankdict['user']=i
        rankdict['username']=i.username
        rankdict['email']=i.email
        for j in l:
            if j.has_key('points') and str(j['subj'])==str(i.email):
                points=points + j['points']
        rankdict['points']=points
        ranklist.append(rankdict)
        rankdict={}
        
    newranksort = sorted(ranklist, key=itemgetter('points'), reverse=True)
    rank=0
    all=PointsRank.objects.all().delete()
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
        except(UserProfile.DoesNotExist):
            pass
    
    return HttpResponse("OK")
    
