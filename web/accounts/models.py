#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField
from sms_utils import send_sms_twilio
import string
import random
import uuid
from emails import send_password_reset_url_via_email
from django.utils.safestring import mark_safe

class ValidSMSCode(models.Model):
    user               = models.ForeignKey(User)
    sms_code           = models.CharField(max_length=4, blank=True)
    expires            = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.sms_code,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        up=self.user.get_profile()
        randcode=random.randint(1000,9999)
        if not self.sms_code:
            self.sms_code=randcode
        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires
        new_number="+1%s" %(string.replace(str(up.mobile_phone_number),"-", ""))
        #send an sms code
        x=send_sms_twilio(twilio_body=self.sms_code, twilio_to=new_number)
        super(ValidSMSCode, self).save(**kwargs)


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

USER_TYPE_CHOICES =          ( ('member',  'Member'),
                             ('organization',  'Organization'),)

ORGANIZATION_CHOICES= ( ('non-profit',  'Non-Profit'),
                         ('for-profit',  'For Profit'),
                         ('individual',  'Individual'))

APPROVAL_CHOICES =( ('pending',  'Pending'),
                         ('approved',  'Approved'),
                         ('rejected',  'rejected'))

SECURITY_CHOICES = (('1',  '1'),
                    ('2',  '2'),
                    ('3',  '3'),
                    ('4',  '4'),
                    )

# Security Choice   1 = Member      - Standard Account
#                   2 = Delegate    - Limited rights given by Owner to manage organization account
#                   3 = Owner       - Organization Account Owner
#                   4 = Staff       - Site Staff Admin - delegated by Site Super Admin
#                   5 = SuperAdmin  - Site Super Admin


class UserProfile(models.Model):
    user_type       = models.CharField(default="member", max_length=10,
                                               choices=USER_TYPE_CHOICES)
    url             = models.URLField(blank = True)
    security_level  = models.CharField(default='1',
                                       choices=SECURITY_CHOICES,
                                       max_length=1)
    approval_status = models.CharField(max_length=10,
                                       choices=APPROVAL_CHOICES,
                                       default='pending')
    phone_number     = PhoneNumberField(blank = True, max_length=15)
    twitter          = models.CharField(blank = True, max_length=15)
    notes            = models.CharField(blank = True, max_length=250)
    user = models.ForeignKey(User, unique=True,)

    # user = models.ForeignKey(User, unique=True, edit_inline=models.TABULAR, num_in_admin=1,
    #                           min_num_in_admin=1, max_num_in_admin=1,num_extra_on_change=0)

    def __unicode__(self):
        return '%s %s is a %s and their status is %s' % (self.user.first_name,
                                self.user.last_name,
                               self.user_type, self.approval_status )
        
    class Meta:
        unique_together = (("user", "user_type"),)

# Now, in views.py, to access a user's profile, you only need two lines:
# user = User.objects.get(pk = user_id)
# user.userprofile = get_or_create_profile(user)
#
# And, say if you wanted to change a value:
# user.userprofile.security_level = '1'
# user.userprofile.save()






permission_choices=(    ('provider',  'provider'),
                        ('tester',  'tester'),
                        ('outreach',    'outreach'),
                        ('member_navigator',  'member_navigator'),
                        ('admin',  'admin'),
                        ('reporter',  'reporter'),

                    )

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
        

        