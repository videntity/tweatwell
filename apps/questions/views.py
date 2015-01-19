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
from models import Question, Answer, CorrectAnswerPoints, CurrentQuestion
from ..accounts.models import UserProfile
@login_required
def question_answer(request):
    # get this week's question
    this_weeks_qtn = CurrentQuestion.objects.get(pk=1)
    
    try:
        question = Question.objects.get(pk=this_weeks_qtn.question_index)
    except(Question.DoesNotExist):
        question = Question.objects.all().order_by('?')[0]
    QuizForm = quiz_form_factory(question)
    profile=request.user.get_profile()
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():  
            data = form.cleaned_data
            print data
            #is the question correct or not?
            if data['answers'].is_correct==True:
                messages.success(request,"You got the question right!")
                profile.qow_status="CORRECT"
                CorrectAnswerPoints.objects.create(user=request.user)
                
            else:
                
                correct_answer = Answer.objects.get(question=question, is_correct=True)
                msg = "Sorry.  %s is incorrect. The correct answer is: %s. Be sure and try again next week!" % \
                        (data['answers'], correct_answer)
                
                messages.success(request,msg)
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