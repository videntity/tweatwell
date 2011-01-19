from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from registration.models import RegistrationProfile
from tweatwell.accounts.models import *
from tweatwell.accounts.forms import AccountSettingsForm
from tweatwell.accounts.emails import send_reply_email
from django.core.urlresolvers import reverse
from tweatwell.accounts.utils import verify
    
@login_required
def account_settings(request):
    updated = False
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            profile.twitter = data['twitter']
            profile.gender= data['gender'] 
            request.user.save()
            profile.save()
            #Add RESTCat Update Here
            
            message='Your account settings have been updated.'
            request.user.message_set.create(
                message='Your account settings have been updated.')
            message='Your account settings have been updated.'
            return render_to_response('registration/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user,
                                              'updated' : message
                                              }))

    else:
        form = AccountSettingsForm({
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'gender': profile.gender,
            'twitter': profile.twitter,
        })

    return render_to_response('registration/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user}))

def verify_email(request, verification_key,
                 template_name='registration/activate.html',
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
