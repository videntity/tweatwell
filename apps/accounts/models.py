#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from localflavor.us.models import PhoneNumberField
import string, random, uuid
from emails import send_password_reset_url_via_email, send_signup_key_via_email
from django.utils.safestring import mark_safe
from restcat_utils import create_restcat_user
from ..checkin.models import FREGGIE_CHOICES

USER_CHOICES     = ( ('player',  'player'), ('admin',  'admin'),)


QOW_CHOICES =   (('NO_ANSWER',  'NO_ANSWER'),
                ('CORRECT',  'CORRECT'),
                ('INCORRECT',  'INCORRECT'),)


FREGGIE_GOAL_CHOICES = ( (1,'1'), (2,'2'),(3,'3'), (4,'4'), (5,'5'),
                         (6,'6'), (7,'7'),(8,'8'), (9,'9'), (10,'10'))

class UserProfile(models.Model):
    user                    = models.ForeignKey(User, unique=True)
    anonymous_patient_id    = models.CharField(max_length=30,       
                                unique=True,  blank=True,
                                verbose_name=u'Anonymous Patient ID')
    user_type               = models.CharField(default='player',
                                choices=USER_CHOICES,
                                max_length=6)
    url                     = models.URLField(blank = True)
    daily_freggie_goal      = models.IntegerField(max_length=1, default=5,
                                choices=FREGGIE_GOAL_CHOICES,
                                verbose_name= 'Daily Fruit and Vegetable "Freggie" Goal')
    twitter                 = models.CharField(blank = True, max_length=15)
    notes                   = models.TextField(blank = True, max_length=250)
    joker_badge             = models.BooleanField(default = False)
    dean_veggie_badge       = models.BooleanField(default = False)
    dean_fruit_badge        = models.BooleanField(default = False)
    president_badge         = models.BooleanField(default = False)
    professor_badge         = models.BooleanField(default = False)
    professor_of_freggie    = models.CharField(choices=FREGGIE_CHOICES,
                                    max_length=20, blank=True, null=True)
    qow_status              = models.CharField(choices=QOW_CHOICES,
                                    max_length=20, default="NO_ANSWER")

    def __unicode__(self):
        return '%s %s is a %s. Active=%s' % (self.user.first_name,
                            self.user.last_name,
                               self.user_type, self.user.is_active )
        
    class Meta:
        unique_together = (("user", "user_type"),
            ("professor_badge","professor_of_freggie"))


    def last_login(self):
        return self.user.last_login

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
        expires=now+timedelta(days=settings.PASSWORD_RESET_TIMEOUT_DAYS)
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



          