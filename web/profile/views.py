# Create your views here.

import sys, types
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from tweatwell import settings
from tweatwell.accounts.models import UserProfile
from tweatwell.web.utils import handle_uploaded_file, query_restcat
from tweatwell.web.coachespoll.models import MaleCoachesPoll, FemaleCoachesPoll
from tweatwell.web.pointsrank.models  import PointsRank

import datetime, os
import pycurl
import StringIO, json, types


def profiles(request):
    profilelist=[]
    users = User.objects.all()
    for u in users:
        try:
            p=u.get_profile()
            if p.annon=="Public":
                profilelist.append(u)
        except(UserProfile.DoesNotExist):
            pass
    
    return render_to_response(
            'profiles/index.html',
            {'profilelist':profilelist,},
            context_instance = RequestContext(request),)    

@login_required
def coaches_profile_list(request):
    p = request.user.get_profile()
    if p.coach==False:
        return HttpResponse("You are not authorized to see this page", status=401)
    profilelist=[]
    users = User.objects.all()
    for u in users:
        try:
            p=u.get_profile()
            profilelist.append(u)
        except(UserProfile.DoesNotExist):
            pass
    
    return render_to_response(
            'profiles/index.html',
            {'profilelist':profilelist,},
            context_instance = RequestContext(request),) 


def user_profile(request, user):
    try:
        u=User.objects.get(username=user)
        p=u.get_profile()
    except(User.DoesNotExist):
        return HttpResponse("User does not exist.", status=404)
    
    if p.annon!="Public" and p.coach==False:
        return HttpResponse("This user's profile is private.", status=400)
    
    ideal_high=2
    ideal_low=1
    guage_max=1
    guage_min=1
    bmi=20
    height=40
    all={'checkins': 0, 'points': 0,
         'gems': 0, 'wt_numeric': 0, 'fm_numeric': 0,
         'pbf_numeric': 0, 'height': 0,
         'pointspoll': 0,
         'femalepbfcpoll':0,
         'malepbfcpoll':0,
         'malecoachespoll':0,
         'femalecoachespoll':0,
         'gender': 0, 'bmi':0, 
         'ideal_high':2,
         'ideal_low':1,
         'guage_max':1,
         'guage_min':1,}
    
    responsedict={'bodylist':0}
    latest_wt={'wt_numeric': 0,
               'wt_measure_unit':'l',
               'ev_dt': None,
               'ev_tz': None,
               }

    all['gender']=p.gender
    weight_goal=p.weight_goal    
        
    try:
        pr=PointsRank.objects.get(user=u)
        all['pointspoll']=pr.rank
    except(PointsRank.DoesNotExist):
        all['pointspoll']=0
        
    try:    
        if (str(p.gender) == "female"):
            cp=FemaleCoachesPoll.objects.get(user=u)
            all['femalecoachespoll']=cp.rank
        else:
            all['femalecoachespoll']=0
    except(FemaleCoachesPoll.DoesNotExist):
        all['femalecoachespoll']=0
    
    try:
        if (str(p.gender) == "male"):
            cp=MaleCoachesPoll.objects.get(user=u)
            all['malecoachespoll']=cp.rank            
        else:
            all['malecoachespoll']=0
    except(MaleCoachesPoll.DoesNotExist):
        all['malecoachespoll']
        
    #get the bfp rank
    try:    
        if (str(p.gender) == "female"):
            r=FemaleBFCRank.objects.get(user=u)
            all['femalepbfcpoll']=r.rank
        else:
            all['femalepbfcpoll']=0
    except(FemaleBFCRank.DoesNotExist):
        all['femalepbfcpoll']=0
    
    try:
        if (str(p.gender) == "male"):
            r=MaleBFCRank.objects.get(user=u)
            all['malepbfcpoll']=r.rank            
        else:
            all['malecoachespoll']=0
    except(MaleBFCRank.DoesNotExist):
        all['malepbfcpoll']
    
    try:
        #get every transaction for this user
        URL="%sapi/omhe/all/%s/" % (settings.RESTCAT_SERVER, u.email)
        responsedict=query_restcat(URL)
        #print responsedict
        if responsedict['code']==200:
            wt_list=[]
            bp_list=[]
            num_transactions=len(responsedict['bodylist'])
            all['checkins']=num_transactions
            for j in responsedict['bodylist']:
                if type(j)==dict:
                    if j.has_key('wt_numeric'):	
                        latest_wt={}
                        latest_wt['wt_numeric']="%.1f" % (float(j['wt_numeric']))
                        latest_wt['wt_measure_unit']=j['wt_measure_unit']
                        latest_wt['ev_dt']=j['ev_dt']
                        latest_wt['ev_tz']=j['ev_tz']
                        
                        #precalculate some numbers to make it easy to display.    
                        height=p.height_in
                        
                        bmi=(float(latest_wt['wt_numeric']) * 703) / (float(p.height_in) * float(p.height_in))
                        bmi="%.1f" %(bmi)
                        ideal_low= (18.6*float(p.height_in) * float(p.height_in))/703
                        ideal_low="%.1f" % (ideal_low)
                        ideal_high=(24.9*float(p.height_in) * float(p.height_in))/703
                        ideal_high="%.1f" % (ideal_high)
                        guage_min = float(ideal_low) - 50.0
                        
                        if (guage_min < 0):
                            guage_min=0.0
                        
                        guage_max=float(ideal_high) + 50.0
                        
                        if guage_max < float(j['wt_numeric']):
                            guage_max= float(j['wt_numeric']) + 50
                            
                        if guage_min > float(j['wt_numeric']):
                            guage_min= float(ideal_low) - 20
    
                        all['wt_numeric']=j['wt_numeric']
                        wt_list.append(latest_wt)
                        all['wt_measure_unit']=j['wt_measure_unit']
                        all['bmi']=(float(all['wt_numeric']) * 703) / (float(p.height_in) * float(p.height_in))
                        all['bmi']="%.2f" %(all['bmi'])                	
                    
                    if j.has_key('fm_numeric'):
                        all['fm_numeric']= j['fm_numeric']
                        
                    if j.has_key('bp_syst'):
                        all['bp']="Systolic: %s,  Diastolic: %s" % (j['bp_syst'], j['bp_dia'])
                                                                         
                    if j.has_key('points'):
                        all['points']=all['points'] + j['points']
                            
                    #if j.has_key('pbf_numeric'):
                    #    all['pbf_numeric']=j['pbf_numeric']
                        
                    if j.has_key('ffm_numeric'):
                        all['ffm_numeric']=j['ffm_numeric']
                        
                    if j.has_key('fm_numeric'):
                        all['fm_numeric']=j['fm_numeric']
                    
                    if j.has_key('ci_payload') and not j.has_key('idr'):
                        all['status']=j['ci_payload']
               
        else:
            msg="Error Fetching your data: HTTPCODE=%s %s" % (
                                        str(responsedict['code']),
                                        str(responsedict['bodylist']))
            error=msg
        all['pbf_numeric']= float(all['fm_numeric']) / float(all['wt_numeric'])*100
        all['pbf_numeric']="%.1f" % (all['pbf_numeric'])
       
        
        return render_to_response(
            'index.html',
            {
            'all': all,
            'latest_wt' : latest_wt,
            'ideal_low' : ideal_low,
            'ideal_high' : ideal_high,
            'guage_min':guage_min,
            'guage_max': guage_max,
            'bmi' : bmi,
            'height' : height,
            'weight_goal': weight_goal,
             },
            context_instance = RequestContext(request),)    
            
    except:
        msg="""Something went wrong. HTTP/500."""
        error= msg + str(sys.exc_info())
        print error
        return render_to_response(
            'index.html',
            {'error':error,
             'ci': responsedict['bodylist'],
            'all': all,
            'latest_wt' : latest_wt,
            'ideal_low' : ideal_low,
            'ideal_high' : ideal_high,
            'guage_min':guage_min,
            'guage_max': guage_max,
            'bmi' : bmi,
            'height' : height,
            'weight_goal': weight_goal,},
            context_instance = RequestContext(request),)
    
    
    return HttpResponse("ok")
    
    
   
