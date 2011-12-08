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
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from models import *
from forms import *
from emails import send_reply_email
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from utils import validate_signup
from models import ValidPasswordResetKey, UserProfile
from datetime import datetime
# from registration.models import RegistrationProfile


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
                print "here"
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
        form = SignupForm(request.POST)
        if form.is_valid():
          new_user = form.save()
          messages.success(request, "Signup complete. Please verify your email.")
          return render_to_response('accounts/signup-complete.html',
                                      RequestContext(request, {}))
        else:
            #return the bound form with errors
            return render_to_response('accounts/signup.html',
                                      RequestContext(request, {'form': form}))      
    else:  
       #this is an HTTP  GET
       return render_to_response('accounts/signup.html',
                                 RequestContext(request,
                                {'form': SignupForm()}))         


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
            try:
                u=User.objects.get(email=data['email'])
            except(User.DoesNotExist):
                messages.error(request, "A user with the email supplied does not exist.")
                return render_to_response('accounts/password-reset-request.html',
                              RequestContext(request,
                                             {'form': form,
                                              }))
            #success so create a 
            k=ValidPasswordResetKey.objects.create(user=u)

            return render_to_response('accounts/reset-token-sent.html',
                              RequestContext(request,
                                             {}))
    else:
        return render_to_response('accounts/password-reset-request.html', 
                             {'form': PasswordResetRequestForm()},
                              RequestContext(request))
    







@login_required
def account_settings(request):

    up = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #update the user info
            request.user.username   = data['username']
            request.user.email       = data['email']
            request.user.first_name = data['first_name']
            request.user.last_name  = data['last_name']  
            request.user.save()
            #update the user profile
            up.twitter            = data['twitter']
            up.mobile_phone_number= data['mobile_phone_number']
            up.save()
            messages.success(request,'Your account settings have been updated.')  
            return render_to_response('accounts/account_settings.html',
                            {'form': form,},
                            RequestContext(request))
        else:
            #the form had errors
            return render_to_response('accounts/account_settings.html',
                            {'form': form,},
                            RequestContext(request))
               

    #this is an HTTP GET        
    return render_to_response('accounts/account_settings.html',
        {'form': AccountSettingsForm(initial={ 'username':request.user.username,
                                'email':request.user.email,
                                'last_name':request.user.last_name,
                                'first_name':request.user.first_name,
                                'twitter':up.twitter,
                                'mobile_phone_number':up.mobile_phone_number,
                                })},
                              RequestContext(request))




def signup_verify(request, signup_key=None):
    
    if validate_signup(signup_key=signup_key):
        messages.success(request, "Your account has been activated.")
        return HttpResponseRedirect(reverse('simple_login'))
    else:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    



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
            messages.success(request, "Your password was reset successfully.")
            return HttpResponseRedirect(reverse('simple_login'))

        else:
         return render_to_response('accounts/reset-password.html',
                        RequestContext(request, {'form': form,
                            'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))




