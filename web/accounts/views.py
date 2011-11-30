#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# accounts.views.py
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from models import *
from forms import AccountSettingsForm, LoginForm, SMSCodeForm, PasswordResetRequestForm, PasswordResetForm, SimpleLoginForm, RegistrationForm
from emails import send_reply_email
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from utils import verify
from models import ValidSMSCode, ValidPasswordResetKey
from datetime import datetime
# from registration.models import RegistrationProfile


def register(request):
    
    return render_to_response('accounts/register.html',
                              {},
                              context_instance = RequestContext(request))

def mylogout(request):
    logout(request)
    return render_to_response('accounts/logout.html',
                              context_instance = RequestContext(request))

    
def simple_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            smscode  = form.cleaned_data['smscode']
            if not validate_sms(username=username, smscode=smscode):
                return HttpResponse("Invalid Access Code")
            
            user=authenticate(username=username, password=password)
            
            if user is not None:

                if user.is_active:
                    login(request,user)
                    messages.success(request, "Logged in successfully.")
                    return HttpResponseRedirect(reverse('home'))
                else:
                   messages.error(request, "Your account is inactive so you may not log in.")
                   return render_to_response('accounts/login.html',
                                            {'form': form},
                                            RequestContext(request))
            else:
                messages.error(request, "Invalid username or password.")
                return render_to_response('accounts/login.html',
                                    {'form': form},
                                    RequestContext(request))

        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    
    #this is a GET
    return render_to_response('accounts/login.html',
                              {'form': LoginForm()},
                              context_instance = RequestContext(request)) 

def signup(request):
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          new_user = form.save()
          return HttpResponseRedirect(reverse('home')) 
    else:  
       username = 'Username'
       email = 'sample.name@example.com'
       first_name = 'firstname'
       last_name = 'lastname' 
       form = UserCreationForm()
       return render_to_response('accounts/signup.html', RequestContext(request, {'form': form}))         
    result = account_settings(request)
    return render_to_response('accounts/account_settings.html', context_instance = RequestContext(request)) 


def reset_password(request, reset_password_key=None):
    try:
        vprk=ValidPasswordResetKey.objects.get(
                                        reset_password_key=reset_password_key)
        
    except:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            return render_to_response('accounts/reset-password-success.html',
                              RequestContext(request,{}))
        else:
         return render_to_response('accounts/reset-password.html',
                        RequestContext(request, {'form': form,
                            'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))
        






def password_reset_request(request):
    if request.method == 'POST':

        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            return render_to_response('accounts/password-reset-request.html',
                              RequestContext(request,
                                             {'form': form,
                                              }))
    else:
        return render_to_response('accounts/password-reset-request.html', 
                             {'form': PasswordResetRequestForm()},
                              context_instance = RequestContext(request))
    






@login_required
def account_settings(request):

    up = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.first_name= data['first_name']
            request.user.last_name= data['last_name']  
            request.user.save()
            up.twitter = data['twitter']
            up.mobile_phone_number= data['phone_number']
            up.save()
            messages.success(request,'Your account settings have been updated.')  
            return render_to_response('accounts/account_settings.html',
                            {'form': form,},
                            RequestContext(request))
        else:
            messages.success(request,'Oops.  Please correct the errors below.')
            return render_to_response('accounts/account_settings.html',
                            {'form': form,},
                            RequestContext(request))
            
                
                

    #this is an HTTP GET        
    return render_to_response('accounts/account_settings.html',
                              {'form': AccountSettingsForm()},
                              RequestContext(request))

def verify_email(request, verification_key,
                 template_name='accounts/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                                context_instance=context)


def get_or_create_profile(user):
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        #create profile - CUSTOMIZE THIS LINE TO OYUR MODEL:
        profile = UserProfile(user=user)
        profile.save()
    return profile
