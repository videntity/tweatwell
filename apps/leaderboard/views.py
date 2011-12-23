#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..accounts.models import UserProfile
from ..checkin.models import Freggie, BadgePoints
from ..checkin.freggies import fruit_tuple, veg_tuple
def score(request):
    # reset all badges
    up = UserProfile.objects.all()
    for u in up:
        u.joker_badge           = False
        u.dean_veggie_badge     = False
        u.dean_fruit_badge      = False
        u.president_badge       = False
        u.professor_badge       = False
        u.professor_of_freggie  = None
        u.save()
    
    # who had the most freggies of all (president)?
    agg = Freggie.objects.values('user').annotate(Sum('quantity')).order_by('-quantity__sum')
    presuser_pk= agg[0]['user']
    president=UserProfile.objects.get(user=presuser_pk)
    president.president_badge = True
    president.save()
    # Give 5 points to the president
    BadgePoints.objects.create(user=president.user, badge='president')
    
    
    # who had the most veggies (excluding the president) ?  - dean of veg 
    agg = Freggie.objects.filter(fruit_or_veg="veg").exclude(user=presuser_pk).values('user').annotate(Sum('quantity')).order_by('-quantity__sum')
    dean_veggie_pk= agg[0]['user']
    dean_veggie=UserProfile.objects.get(user=dean_veggie_pk)
    dean_veggie.dean_veggie_badge = True
    dean_veggie.save()
    # Give 5 points to the dean
    BadgePoints.objects.create(user=dean_veggie.user, badge='vegdean')
    
    # who had the most fruits (excluding the president & veg dean)?  - dean of fruit
    agg = Freggie.objects.filter(fruit_or_veg="fruit").exclude(user=presuser_pk).exclude(user=dean_veggie_pk).values('user').annotate(Sum('quantity')).order_by('-quantity__sum')
    dean_fruit_pk= agg[0]['user']
    dean_fruit=UserProfile.objects.get(user=dean_fruit_pk)
    dean_fruit.dean_fruit_badge = True
    dean_fruit.save()
    # Give 5 points to the dean
    BadgePoints.objects.create(user=dean_fruit.user, badge='fruitdean')

    professor_list=[]
    for f in fruit_tuple:
        
        agg = Freggie.objects.filter(freggie=f).values('user').annotate(Sum('quantity')).order_by('-quantity__sum')
        if agg:
            print "Professor of ", f, " is ", agg[0]['user']
            professor_pk = agg[0]['user']
            professor=UserProfile.objects.get(user=professor_pk)
            professor.professor_badge = True
            professor.professor_of_freggie=f
            professor.save()
            professor_list.append({'freggie':f, 'professor':professor})
            BadgePoints.objects.create(user=professor.user, badge='professor')
    
    return render_to_response('leaderboard/score.html',
            {'dean_fruit':dean_fruit,
             'dean_veggie':dean_veggie,         
            'president':president,         
             'professor_list':professor_list},
            context_instance = RequestContext(request),)

def leaderboard(request):
    return render_to_response('leaderboard/index.html',
            {},
            context_instance = RequestContext(request),)    
    
