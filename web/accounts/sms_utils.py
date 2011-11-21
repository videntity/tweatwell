#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
import twilio


def send_sms_twilio(twilio_body, twilio_to,
                    twilio_from=settings.TWILIO_DEFAULT_FROM):
    
    account = twilio.Account(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    d = {
    'From' : twilio_from,
    'To' : twilio_to,
    'Body': twilio_body
    }
    
    try:
        x= account.request('/%s/Accounts/%s/SMS/Messages.json' % \
                                (settings.TWILIO_API_VERSION,
                                 settings.TWILIO_SID), 'POST', d)
        return x
    except Exception, e:
        print e
        print e.read()
        return None