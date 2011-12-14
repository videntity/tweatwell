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
from ..accounts.models import UserProfile, Award
from ..questions.models import QuestionAnswer, Question
from forms import FreggieForm, CommentForm
from ..upload.forms import PickFruitForm, PickVeggieForm
import datetime, os, pycurl, StringIO, json, types, sys
from operator import itemgetter, attrgetter
from django.contrib import messages
from models import Comment, Freggie
from ..roulette.models import Roulette
from django.db.models import Sum



def anon_home_index(request):
    print ("anonymous home. We'll do this at near the end. for now redirect to login/signup")
    return HttpResponseRedirect(reverse('simple_login'))

@login_required
def answer_question(request):
    pass


@login_required
def freggie_comment(request, freggie_id):
    
    freggie = get_object_or_404(Freggie, pk=freggie_id)
    
    if request.method == 'POST':

        form = CommentForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newcomment=form.save(commit=False)
            newcomment.text=data['text']
            newcomment.user=request.user
            newcomment.freggie=freggie
            newcomment.save()
            messages.success(request, "Successfuly added a comment.")
            return HttpResponseRedirect(reverse('checkin'))
            
def checkin(request):


    commentform=CommentForm()
    #if the user is not logged in, display an anonymous home page
    if request.user.is_anonymous()==True:
        return anon_home_index(request)
    
    u=User.objects.get(username=request.user)
    p=get_object_or_404(UserProfile, user=u)
    awards =Award.objects.filter(user=u)
    question=Question.objects.get(display=True)
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
        
    #fetch points
    
    freggie_points = Freggie.objects.filter(user=request.user).aggregate(Sum('points'))
    if freggie_points['points__sum']== None:
        freggie_points['points__sum']=0
    
    comment_points = Comment.objects.filter(user=request.user).aggregate(Sum('points'))
    if comment_points['points__sum']== None:
        comment_points['points__sum']=0    

    spin_points = Roulette.objects.filter(user=request.user).aggregate(Sum('points'))
    if spin_points['points__sum']== None:
        spin_points['points__sum']=0
        
    roulette_points = Comment.objects.filter(user=request.user).aggregate(Sum('points'))
    if roulette_points['points__sum']== None:
        roulette_points['points__sum']=0 
    
    
    points = freggie_points['points__sum'] + comment_points['points__sum'] + \
                spin_points['points__sum'] + roulette_points['points__sum']
    
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
        form = FreggieForm(request.POST)
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
                 'question':question,
                'deanaward':DeanAward,
                'tweatlist': tweatlist,
                'commentform': commentform,
                'presidentaward':PresidentAward,
                'professoraward': ProfessorAward,
                'freggies': freggies,
                'points': points,},
                context_instance = RequestContext(request),)

    return render_to_response('checkin/checkin.html',
            {'form': FreggieForm(),
             'question': question,
             'deanaward': DeanAward,
             'tweatlist': tweatlist,
             'commentform': commentform,
             'presidentaward':PresidentAward,
             'professoraward': ProfessorAward,
             'freggies': freggies,
             'points': points,
            },
            context_instance = RequestContext(request),)