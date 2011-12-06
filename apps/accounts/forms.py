#!/usr/bin/env python
from django import forms
from  models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from django.conf import settings


class PasswordResetRequestForm(forms.Form):
    email= forms.CharField(max_length=75, label="Email")

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password (again)*")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2



class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password")






class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password (again)")
    email = forms.EmailField(max_length=75, label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=60, label="Last Name")
    mobile_phone_number = forms.CharField(max_length=15, label="Mobile Phone Number")
    twitter = forms.CharField(max_length=15, label="Twitter")
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


    def save(self, profile_callback=None):
        new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data.get('first_name', "")
        new_user.last_name = self.cleaned_data.get('last_name', "")
        new_user.is_active = False
        new_user.save()
        up=UserProfile.objects.create(
            user=new_user,
            twitter=self.cleaned_data.get('twitter', ""),
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            )
        v=ValidSignupKey(user=new_user)
        v.save()
        return new_user

class AccountSettingsForm(forms.Form):
    username = forms.CharField(max_length=30, label="Userame")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=60, label="Last Name")
    mobile_phone_number = forms.CharField(max_length=15, label="Phone Number")
    twitter = forms.CharField(max_length=15, label="Twitter")
     
    def clean_twitter(self):
        twitter = self.cleaned_data.get("twitter", "")
        if twitter!="":
            if twitter[0:1]=="@":
                twitter=twitter[1:]
        return twitter
