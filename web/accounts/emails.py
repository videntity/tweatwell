#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.core.mail import EmailMessage,  EmailMultiAlternatives

def send_reply_email(request, post, form):
    subject = "Someone has replied to '%s' on georegistry.org" % (
        post.title)
    
    sender = request.user.email
    
    body = "In reference to %s, %s said:\n\n%s" % (
        request.build_absolute_uri(post.get_absolute_url()),
        sender,
        form.cleaned_data['content'])
    to = (post.contact.email,)
    headers = {'Reply-To': sender}

    email = EmailMessage(subject=subject,
                         body=body,
                         from_email='gr@georegistry.org',
                         to=to,
                         headers=headers)
    email.send()


def send_password_reset_url_via_email(user, reset_key):
    subject = "Your password reset email from %s." % (settings.ORGANIZATION_NAME)    
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    headers = {'Reply-To': from_email}
    
    html_content = """"
    <P>
    Click on the following link to reset your password.<br>
    <a HREF="%s/accounts/reset-password/%s">%s/accounts/reset-password/%s</a>
    </P>
    """ % (settings.HOSTNAME_URL , reset_key, settings.HOSTNAME_URL, reset_key)
   
    text_content="""
    Click on the following link to reset your password.
    %s/accounts/reset-password/%
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

