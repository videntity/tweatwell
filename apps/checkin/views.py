#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ..accounts.models import UserProfile
from ..utils import handle_uploaded_file, query_restcat
from ..questionstips.models  import QuestionTips
from ..awards.models  import Award
from forms import FreggieForm
from ..upload.forms import PickFruitForm, PickVeggieForm
import datetime, os, pycurl, StringIO, json, types, sys
from operator import itemgetter, attrgetter

def anon_home_index(request):
    print ("anon. we'll do this at near the end. for now redirect to login/signup")
    return HttpResponseRedirect(reverse('simple_login'))

def checkin(request):

    #if the user is logged in, display
    if request.user.is_anonymous()==True:
        return anon_home_index(request)
    
    u=User.objects.get(username=request.user)
    p=get_object_or_404(UserProfile, user=u)
    awards =Award.objects.filter(user=u)

    PresidentAward=False
    ProfessorAward=False
    DeanAward=False
    for a in awards:
        if a.award_class=="President":
            PresidentAward=True
        if a.award_class=="Dean":
            DeanAward=True
        if a.award_class=="Professor":
            ProfessorAward=True    
        
    #fetch freggies and points
    freggies=0
    points=0
    
    if request.method == 'POST':
        form = FreggieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success("Status updated.")
            return HttpResponseRedirect(reverse('checkin'))
        else:
            #the form had errors.
            return render_to_response('checkin/checkin.html',
                {'form':form,
                'deanaward':DeanAward,
                'presidentaward':PresidentAward,
                'professoraward': ProfessorAward,
                'freggies': freggies,
                'points': points,},
                context_instance = RequestContext(request),)

    return render_to_response('checkin/checkin.html',
            {'form':FreggieForm(),
             'deanaward':DeanAward,
             'presidentaward':PresidentAward,
             'professoraward': ProfessorAward,
             'freggies': freggies,
             'points': points,
            },
            context_instance = RequestContext(request),)
