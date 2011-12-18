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
from ..questions.models import QuestionAnswer, Question
from forms import FreggieForm, CommentForm, NonVegForm
from ..upload.forms import PickFruitForm, PickVeggieForm
import datetime, os, pycurl, StringIO, json, types, sys
from operator import itemgetter, attrgetter
from django.contrib import messages
from models import Comment, Freggie, NonVeg
from ..roulette.models import Roulette
from django.db.models import Sum
from itertools import chain
from operator import attrgetter

def anon_home_index(request):
    print ("anonymous home. We'll do this at near the end. for now redirect to login/signup")
    return HttpResponseRedirect(reverse('simple_login'))

@login_required
def answer_question(request):
    pass



@login_required
def admin_profile(request, username):
    u=get_object_or_404(User, username=username)
    p=get_object_or_404(UserProfile, user=u)
    nonvegs=NonVeg.objects.filter(user=u)
    freggies=Freggie.objects.filter(user=u)
    combolist = sorted(chain(nonvegs, freggies), key=attrgetter('evdt'),
                       reverse=True)
    
    return render_to_response('checkin/admin-profile.html',
                    {'combolist':combolist,
                     'u':u,
                     'profile':p
                     },
            context_instance = RequestContext(request),)




@login_required
def profile(request):
    p=get_object_or_404(UserProfile, user=request.user)
    nonvegs=NonVeg.objects.filter(user=request.user)
    freggies=Freggie.objects.filter(user=request.user)
    combolist = sorted(chain(nonvegs, freggies), key=attrgetter('evdt'),
                       reverse=True)
    
    return render_to_response('checkin/profile.html',
                    {
                'freggies': freggies,
                'nonvegs': nonvegs,
                'combolist':combolist,
            },
            context_instance = RequestContext(request),)


@login_required
def nonveg(request):
    
    if request.method == 'POST':

        form = NonVegForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newnonveg=form.save(commit=False)
            newnonveg.text=data['text']
            newnonveg.nonveg=data['nonveg']
            newnonveg.user=request.user
            newnonveg.save()
            messages.success(request, "Successfuly added a non fruit or vegetable item.")
            return HttpResponseRedirect(reverse('checkin'))


@login_required
def freggie_comment(request):
    
    if request.method == 'POST':

        form = NonVegForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newnonveg=form.save(commit=False)
            newnonveg.text=data['text']
            newnonveg.nonveg=data['nonveg']
            newnonveg.user=request.user
            newcomment.save()
            messages.success(request, "Successfuly added a non fruit or vegetable item.")
            return HttpResponseRedirect(reverse('checkin'))
            
def checkin(request):

    #if the user is not logged in, display an anonymous home page
    if request.user.is_anonymous()==True:
        return anon_home_index(request)
    
    u=User.objects.get(username=request.user)
    p=get_object_or_404(UserProfile, user=u)

    question=Question.objects.get(display=True)

        
    #fetch points
    
    freggie_points = Freggie.objects.filter(user=request.user).aggregate(Sum('points'))
    if freggie_points['points__sum']== None:
        freggie_points['points__sum']=0
    
    comment_points = Comment.objects.filter(user=request.user).aggregate(Sum('points'))
    if comment_points['points__sum']== None:
        comment_points['points__sum']=0    

    roulette_points = Roulette.objects.filter(user=request.user).aggregate(Sum('points'))
    if roulette_points['points__sum']== None:
        roulette_points['points__sum']=0
        

    
    points = freggie_points['points__sum'] + comment_points['points__sum'] + \
                roulette_points['points__sum']

    freggie_points =  freggie_points['points__sum']
    comment_points =  comment_points['points__sum']
    roulette_points =  roulette_points['points__sum']

    #fetch total freggies -----------------------------------------------------
    
    freggies=Freggie.objects.filter(user=request.user).count()

    #fetch tweats and comments ------------------------------------------------
    tweats = Freggie.objects.all()
    tweatlist=[]
    for t in tweats:
        c=Comment.objects.filter(freggie=t)
        tweatitem = {'tweat': t, 'comments':c}
        tweatlist.append(tweatitem)
    
    if request.method == 'POST':
        form = FreggieForm(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.user=request.user
            f.save()
            messages.success(request, "Status updated.")
            return HttpResponseRedirect(reverse('checkin'))
        else:
            #the form had errors.
            return render_to_response('checkin/checkin.html',
                {'form':form,
                 'commentform': CommentForm(),
                 'nonvegform': NonVegForm(),
                 'question':question,
                 'tweatlist': tweatlist,
                 'freggies': freggies,
                 'freggie_points': freggie_points,
                 'comment_points': comment_points,
                 'roulette_points': roulette_points,         
                 'points': points},
                context_instance = RequestContext(request),)

    return render_to_response('checkin/checkin.html',
            {'form': FreggieForm(),
                 'commentform': CommentForm(),
                 'nonvegform': NonVegForm(),
                 'question':question,
                'tweatlist': tweatlist,
                'freggies': freggies,
                'freggie_points': freggie_points,
                'comment_points': comment_points,
                'roulette_points': roulette_points,         
                'points': points
            },
            context_instance = RequestContext(request),)