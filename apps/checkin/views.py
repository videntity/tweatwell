#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..accounts.models import UserProfile
from ..questions.models import CorrectAnswerPoints
from ..roulette.models import Roulette
from ..tips.models import CurrentTip
from ..upload.forms import PickFruitForm, PickVeggieForm
import datetime
from forms import FreggieForm, CommentForm
from models import Comment, Freggie
from itertools import chain
from operator import attrgetter
   
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
            
@login_required
def checkin(request):

    
    #if the user is not logged in, display an anonymous home page
    if request.user.is_anonymous()==True:
        return anon_home_index(request)
    
    u=User.objects.get(username=request.user)
    p=get_object_or_404(UserProfile, user=u)
    
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
                 'tweatlist': tweatlist,
                 'freggies': freggies,},
                context_instance = RequestContext(request),)

    return render_to_response('checkin/checkin.html',
            {'form': FreggieForm(),
                 'commentform': CommentForm(),
                'tweatlist': tweatlist,
                'freggies': freggies,},
            context_instance = RequestContext(request),)