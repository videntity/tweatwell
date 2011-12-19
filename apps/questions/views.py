#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import quiz_form_factory
from models import Question, Answer
from ..accounts.models import UserProfile
@login_required
def question_answer(request):
    # start with a random question
    question = Question.objects.all().order_by('?')[0]    
    QuizForm = quiz_form_factory(question)
    profile=request.user.get_profile()
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():  
            data = form.cleaned_data
            
            #is the question correct or not?
            if data['answers'].is_correct==True:
                messages.success(request,"You got the question right!")
                profile.qow_status="CORRECT"
                
            else:
                messages.success(request,
                    "You got the question wrong. Better luck next week!")
                profile.qow_status="INCORRECT"
            profile.save()
            return HttpResponseRedirect(reverse('checkin'))

        else:
            #the form had errors
            return render_to_response('questions/index.html',
                    RequestContext(request,{
                        'question':question,
                        'form':form}))
    else:
        
        
        #this is an HTTP GET
        
        if profile.qow_status == "NO_ANSWER":
            return render_to_response('questions/index.html',
                    RequestContext(request,{
                        'question':question,
                        'form':QuizForm()}))
        else:
            return render_to_response('questions/index.html',
                    RequestContext(request,{
                        'question':question,
                        'already_answered':"You've already answered this week's question. Try back next week."}))