#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField
import string, random, uuid
from emails import send_password_reset_url_via_email, send_signup_key_via_email
from django.utils.safestring import mark_safe
from restcat_utils import create_restcat_user
from ..checkin.models import FREGGIE_CHOICES

USER_CHOICES     = ( ('player',  'player'),
                    ('admin',  'admin'),
                    )

award_choices=(
        ('President','President'), ('Dean','Dean'), ('Professor','Professor'),
        )

class Award(models.Model):
    user  = models.ForeignKey(User)
    award_class = models.CharField(max_length=15, choices=award_choices)
    freggie = models.CharField(max_length=40,
                               choices=FREGGIE_CHOICES,
                               blank=True)
    points = models.IntegerField(max_length=2, default=10)

    
    def __unicode__(self):
        return '%s is the %s of %s' % (self.user.username,
       		self.award_class, self.freggie)
    class Meta:
        unique_together = (("award_class", "freggie"),)  


class UserProfile(models.Model):
    user                    = models.ForeignKey(User, unique=True)
    anonymous_patient_id    = models.CharField(max_length=30,       
                                  unique=True,
                                  verbose_name=u'Anonymous Patient ID',
                                  blank=True)
    url                     = models.URLField(blank = True)
    user_type               = models.CharField(default='player',
                                       choices=USER_CHOICES,
                                       max_length=6)
    mobile_phone_number     = PhoneNumberField(blank = True, max_length=15)
    daily_freggie_goal      = models.IntegerField(max_length=1, default=5)
    twitter                 = models.CharField(blank = True, max_length=15)
    notes                   = models.TextField(blank = True, max_length=250)
    awards                  = models.ManyToManyField(Award, blank = True, null=True)



    def __unicode__(self):
        return '%s %s is a %s. Active=%s' % (self.user.first_name,
                            self.user.last_name,
                               self.user_type, self.user.is_active )
        
    class Meta:
        unique_together = (("user", "user_type"),)

    def save(self, **kwargs):
        if not self.anonymous_patient_id:
            self.anonymous_patient_id = str(uuid.uuid4())[0:30]

        
        #response=create_restcat_user(username=self.anonymous_patient_id,
        #                    password=str(uuid.uuid4())[0:30],
        #                    email=self.user.email,
        #                    first_name=self.user.first_name,
        #                    last_name=self.user.last_name,
        #                    mobile_phone_number=self.mobile_phone_number)
        super(UserProfile, self).save(**kwargs)









class ValidPasswordResetKey(models.Model):
    user               = models.ForeignKey(User)
    reset_password_key = models.CharField(max_length=50, blank=True)
    expires            = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.reset_password_key,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        
        self.reset_password_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires
        
        #send an email with reset url
        x=send_password_reset_url_via_email(self.user, self.reset_password_key)
        super(ValidPasswordResetKey, self).save(**kwargs)


class ValidSignupKey(models.Model):
    user                 = models.ForeignKey(User)
    signup_key           = models.CharField(max_length=50, blank=True,
                                            unique=True)
    expires              = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.signup_key,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        
        self.signup_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(days=settings.SIGNUP_TIMEOUT_DAYS)
        self.expires=expires
        
        #send an email with reset url
        x=send_signup_key_via_email(self.user, self.signup_key)
        super(ValidSignupKey, self).save(**kwargs)






class ValidPasswordResetKey(models.Model):
    user               = models.ForeignKey(User)
    reset_password_key = models.CharField(max_length=50, blank=True)
    expires            = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.reset_password_key,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        
        self.reset_password_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires
        
        #send an email with reset url
        x=send_password_reset_url_via_email(self.user, self.reset_password_key)
        super(ValidPasswordResetKey, self).save(**kwargs)











permission_choices=(    ('player',  'player'),
                        ('admin',  'admin'),)

class Permission(models.Model):
    user  = models.ForeignKey(User)
    permission_name = models.CharField(max_length=50,
                                       choices=permission_choices)

    def __unicode__(self):
        return '%s %s has the %s permission.' % (self.user.first_name,
                                                 self.user.last_name,
                                                 self.permission_name)
        
    class Meta:
        unique_together = (("user", "permission_name"),)
        

def validate_signup(signup_key):
    try:
        vc=ValidSignupKey.objects.get(signup_key=signup_key)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False   
    except(ValidSignupKey.DoesNotExist):
        return False  
    u=vc.user
    u.is_active=True
    u.save()
    vc.delete()
    return True



          