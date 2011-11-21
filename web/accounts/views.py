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
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            user=authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                   return HttpResponse("Inactive Account")
            else:
                return HttpResponse("Invalid Username or Password")
            return HttpResponse("Authenticate, send SMS, & redirect to SMSCode")
        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/login.html',
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
    


def validate_sms(username, smscode):
    try:
        u=User.objects.get(username=username)
        vc=ValidSMSCode.objects.get(user=u, sms_code=smscode)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        return False        
    except(ValidSMSCode.DoesNotExist):
        return False  
    vc.delete()
    return True


def sms_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print "Authenticate"
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            smscode  = form.cleaned_data['smscode']
            if not validate_sms(username=username, smscode=smscode):
                return HttpResponse("Invalid Access Code")
            
            user=authenticate(username=username, password=password)
            
            if user is not None:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                   return HttpResponse("Inactive Account")
            else:
                return HttpResponse("Invalid Username or Password")
            return HttpResponse("Authenticate, send SMS, & redirect to SMSCode")
        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/login.html',
                              context_instance = RequestContext(request)) 

def sms_code(request):
    if request.method == 'POST':
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            try:
                u=User.objects.get(username=form.cleaned_data['username'])
                up=u.get_profile()
                ValidSMSCode.objects.create(user=u)
            except(User.DoesNotExist):
                return HttpResponse("You are not recognized.", status=401)
            except(UserProfile.DoesNotExist):
                return HttpResponse("You do not have a user profile.", status=401)
            
            return HttpResponseRedirect(reverse('login'))
        else:
         return render_to_response('accounts/smscode.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request)) 

@login_required
def account_settings(request):
   updated = False
   # up = get_object_or_404(UserProfile, user=request.user)
   try:
       up = UserProfile.objects.get(user=request.user)
       print "update" 
       create=False
   except(UserProfile.DoesNotExist):
       create=True
   
   #  profile = request.user.get_profile()
   if request.method == 'POST':
         form = AccountSettingsForm(request.POST)
         if form.is_valid():
            print "Valid form"
            data = form.cleaned_data
            
            request.user.first_name= data['first_name']
            request.user.last_name= data['last_name'] 
            request.user.save()
            
            if create==True:

                up=UserProfile.objects.create(user=request.user)

                up.twitter = data['twitter']
                up.phone_number= data['phone_number']
                up.save()
                messages.info(request,'Your account settings have been created.')  
            #Add RESTCat Update Here
            else:
               
                print "what was that email:"
                user_id = request.user.id
                user = User.objects.get(pk = user_id)
                old_email = user.email
                if (old_email != data['email']):
                        user.email = data['email']
                        user.save()
                up.twitter = data['twitter']
                up.phone_number= data['phone_number']

                up.save()
                messages.info(request,'Your account settings have been updated.')
                
            return HttpResponseRedirect(reverse('home'),)
            #request.user.message_set.create(
            #    message='Your account settings have been updated.')
            #message='Your account settings have been updated.'
            return render_to_response('accounts/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user,
                                              
                                              }))
         else:
            user = User.objects.get(pk = user_id)
            user.userprofile = get_or_create_profile(user)
            print "hit the else - we had errors"
            return render_to_response('accounts/account_settings.html',
                                        RequestContext(request,
                                                       {'form': form,
                                                        'user': request.user,}))    
             
   else:
        print "if GET account_settings_else" 
        if create==True:
            return render_to_response('accounts/account_settings.html',
                                  RequestContext(request,
                                                 {'form': AccountSettingsForm(),
                                                  'user': request.user,}))    
       
        else:
            print "GET but create is false"
            user_id = request.user.id
            print user_id
            user = User.objects.get(pk = user_id)
            user.userprofile = get_or_create_profile(user)
            print user.userprofile

            print "user follows:"
            print user

            form = AccountSettingsForm()
            form.first_name = user.first_name
            form.last_name = user.last_name
            form.phone_number = user.userprofile.phone_number
            form.email = user.email
            form.twitter = user.userprofile.twitter
            print form.first_name + "..." + form.last_name + "..." + form.email

            print "twitter:" + form.twitter
            
            form = AccountSettingsForm({'last_name':form.last_name,
                                        'first_name': form.first_name,
                                        'email': form.email,
                                        'phone_number': form.phone_number,
                                        'twitter': form.twitter,
                                        })
            print form
            return render_to_response('accounts/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user,}))

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
