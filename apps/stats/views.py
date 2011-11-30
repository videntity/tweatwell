# Create your views here.
from django.conf import settings
from django.http import HttpResponse, Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ..utils import query_restcat
import pycurl
import sys, types, os, json, StringIO, datetime



@login_required
def stats_wt(request, user):
    error=None
    u=User.objects.get(username=user)
    p=u.get_profile()
    initial_percent_bodyfat=0
    last_percent_bodyfat=0
    first_wt=0
    first_fm=0
    last_wt=0
    last_fm=0
    fmnum_readings=0
    fmlist=[]
    wtlist=[]
    wtnum_readings=0
    weight_goal=p.weight_goal
    percentchangebodyfat=0
    enough_data=True

    #print json_string
    try:
        #query the server
        URL="%sapi/omhe/find/fm/%s/" % (settings.RESTCAT_SERVER, u.email)
        responsedict=query_restcat(URL)
        fmlist=responsedict['bodylist']
        fmnum_readings=len(responsedict['bodylist'])
        latest_wt={}
        
        URL="%sapi/omhe/find/wt/%s/" % (settings.RESTCAT_SERVER, u.email)
        responsedict=query_restcat(URL)
        wtlist=responsedict['bodylist'] #json_string=json.dumps(json_string)
        wtnum_readings=len(responsedict['bodylist'])

        #the first and last weight
        if type(wtlist[0])==dict:
            first_wt=wtlist[-1]['wt_numeric']
            last_wt=wtlist[0]['wt_numeric']
            if wtlist < 2:
                enough_data=False
        else:
            first_wt=1
            last_wt=1
            enough_data=False
            
        #the first and last fat mass
        if type(fmlist[0])==dict:
            first_fm=fmlist[-1]['fm_numeric']
            last_fm=fmlist[0]['fm_numeric']
            if fmlist < 2:
                enough_data=False
                
        else:
            enough_data=False
            first_fm=1
            last_fm=1
        
        initial_percent_bodyfat= float(first_fm) / float(first_wt)*100
        
        
        last_percent_bodyfat= float(last_fm) / float(last_wt)*100
        
        
        percentchangebodyfat = float(last_percent_bodyfat) / float(initial_percent_bodyfat)-1
        
        if percentchangebodyfat > 1.0:
            percentchangebodyfat = float(initial_percent_bodyfat) / float(last_percent_bodyfat)
        else:
            percentchangebodyfat=percentchangebodyfat * 100
        
        percentchangebodyfat=percentchangebodyfat= "%.2f" % (percentchangebodyfat) 
        initial_percent_bodyfat= "%.1f" % (initial_percent_bodyfat)
        last_percent_bodyfat= "%.1f" % (last_percent_bodyfat)

        #for j in json_string:
        #    latest_wt['wt_numeric']="%.1f" % (float(j['wt_numeric']))
        #    latest_wt['wt_measure_unit']=j['wt_measure_unit']
        #    latest_wt['ev_dt']=j['ev_dt']
        #    latest_wt['ev_tz']=j['ev_tz']
        #    
        #bmi=(float(latest_wt['wt_numeric']) * 703) / (float(p.height_in) * float(p.height_in))
        #bmi="%.1f" %(bmi)
        #ideal_low= (18.6*float(p.height_in) * float(p.height_in))/703
        #ideal_low="%.1f" % (ideal_low)
        #ideal_high=(24.9*float(p.height_in) * float(p.height_in))/703
        #ideal_high="%.1f" % (ideal_high)
        #
        #guage_min = float(ideal_low) - 50.0
        #
        #if (guage_min < 0):
        #    guage_min=0.0
        #guage_max=float(ideal_high) + 50.0
        #
        #if guage_max < float(j['wt_numeric']):
        #    guage_max= float(j['wt_numeric']) + 50
        #    
        #if guage_min > float(j['wt_numeric']):
        #    guage_min= float(ideal_low) - 20
        #
        #num_readings=len(json_string)
        error=None
    except:
        error= str(sys.exc_info())
        json_string={}
        latest_wt=0
        num_readings=0
        bmi=0
        num_readings=0
        enough_data=False
        
    return render_to_response(
            'stats/wt.html',
            {
            'error': error,
            'enough_data': enough_data,
            'percentchangebodyfat':percentchangebodyfat,
            'initial_percent_bodyfat':initial_percent_bodyfat,
            'last_percent_bodyfat':last_percent_bodyfat,
            'first_wt': first_wt,
            'first_fm':first_fm,
            'last_wt':last_wt,
            'last_fm':last_fm,
            'error': error,
            'fmlist' : fmlist,
            'wtlist' : wtlist,
            'latest_wt' : latest_wt,
            'wtnum_readings' : wtnum_readings,
            'fmnum_readings' : fmnum_readings,
            'weight_goal' : weight_goal,
             },
            context_instance = RequestContext(request),)



@login_required
def stats_st(request, user):
    u=User.objects.get(username=user)
    p=u.get_profile()
    URL="%sapi/omhe/find/st/%s/" % (settings.RESTCAT_SERVER, u.email)
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

    try:
        num_readings=0
        json_string=list(json.loads(json_string))
        latest_st={}
        for j in json_string:
            latest_st['st_numeric']=j['st_numeric']
            latest_st['ev_dt']=j['ev_dt']
            latest_st['ev_tz']=j['ev_tz']
            #print j['st_numeric']
            
        num_readings=len(json_string)
    except:
        json_string={},
        latest_st=0,
        num_readings=0
        
    return render_to_response(
            'stats/st.html',
            {
            'stlist' : json_string,
            'latest_st' : latest_st,
            'num_readings' : num_readings,
             },
            context_instance = RequestContext(request),)





@login_required
def stats_bp(request, user):
    u=User.objects.get(username=user)
    URL="%sapi/omhe/find/bp/%s/" % (settings.RESTCAT_SERVER, u.email)
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

    try:
        num_readings=0
        json_string=list(json.loads(json_string))
        latest_bp={}
        bplist=[]
        for j in json_string:
            d={}
            d['bp_syst']=j['bp_syst']
            d['bp_dia']=j['bp_dia']
            d['ev_dt']=j['ev_dt']
            
            bplist.append(d)
    
            latest_bp['bp_syst']=j['bp_syst']
            latest_bp['bp_dia']=j['bp_dia']
            if j.has_key('bp_pul'):
                latest_bp['bp_pul']=j['bp_pul']
            else:
                latest_bp['bp_pul']="Not Given"
            
            latest_bp['ev_dt']=j['ev_dt']
            num_readings=len(bplist)
    
    except:
            bplist=[]
            latest_bp={}
            num_readings=0
        
    return render_to_response(
            'stats/bp.html',
            {
            'bplist':bplist,
            'latest_bp':latest_bp,
            'num_readings':num_readings,
             },
            context_instance = RequestContext(request),)
    