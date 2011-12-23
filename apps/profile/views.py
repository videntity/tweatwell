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
import datetime
from forms import NonVegForm
from models import NonVeg
from ..checkin.models import Freggie, FreggieGoal
from itertools import chain
from operator import attrgetter
from django.forms.models import model_to_dict

@login_required
def profile(request):
    p=get_object_or_404(UserProfile, user=request.user)
    nonvegs=NonVeg.objects.filter(user=request.user)
    freggies=Freggie.objects.filter(user=request.user)
    combolist = sorted(chain(nonvegs, freggies), key=attrgetter('evdt'),
                       reverse=True)
 
    agg = Freggie.objects.values('freggie').annotate(Sum('quantity')).order_by()
    agg = Freggie.objects.filter(user=request.user).values('evdate').annotate(freggie=Sum('quantity')).order_by()
    goallist=[]
    for a in agg:
        goal=FreggieGoal.objects.get(user=request.user, evdate=a['evdate'])
        a['goal']=goal.freggie_goal
        goallist.append(a)
    return render_to_response('profile/profile.html',
            {'goallist':goallist,
            'freggies': freggies,
            'nonvegs': nonvegs,
            'combolist':combolist,
            'nonvegform': NonVegForm(),},
            context_instance = RequestContext(request),)


@login_required
def admin_profile(request, username):
    u=get_object_or_404(User, username=username)
    p=get_object_or_404(UserProfile, user=u)
    nonvegs=NonVeg.objects.filter(user=u)
    freggies=Freggie.objects.filter(user=u)
    combolist = sorted(chain(nonvegs, freggies), key=attrgetter('evdt'),
                       reverse=True)
    
    return render_to_response('profile/admin-profile.html',
                    {'combolist':combolist,
                     'u':u,
                     'profile':p
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
            messages.success(request, "Successfuly added a non-freggie item.")
            return HttpResponseRedirect(reverse('profile'))

