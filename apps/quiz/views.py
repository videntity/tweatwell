import os
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django import forms
from models import *
from forms import TakeQuizForm
import types
from django.db.models import Avg, Count


@login_required
def take_quiz(request, category):
    """This view display a random quiz on GET and processes/grades on POST"""
    
    """get the category object from the category name passed on the url."""
    c=get_object_or_404(Category,slug=category)
    
    if request.method == 'POST': # If the form has been submitted...        
        
        """Make sure we already have a quizid, otherwise redraw the quiz form"""
        try:
            quizid=request.POST['quizid']
            int(quizid)
        except:
            return render_to_response(
            'quiz/take_quiz.html',
            {},
            context_instance = RequestContext(request),)
        
        
        """Get the current quiz object or return 404"""
        q=get_object_or_404(Quiz,id=quizid)
        
        """Get the number of questions for this quiz instance"""
        num_questions=Response.objects.filter(quiz=q).count() 
        """Make sure all the questions were answered"""
        if int(num_questions) != (len(request.POST)-2):
            """
            Was there an answer to every question taking into account the
            hidden quizid form field.  This is why it is one less.
            """
            
            return render_to_response(
                'quiz/incomplete.html',
                {},
                context_instance = RequestContext(request),)        
        else:
            """Figure out how many previous attempts"""
            num_attempts=Quiz.objects.filter(user=request.user)
            num_attempts=num_attempts.count()
        
            """Update the quiz"""
            q.attempt=num_attempts
            q.id=quizid
            q.save(force_update=True)
        
        
        """Iterate through the form params"""
        for attr in request.POST:
            if attr == "quizid":
                pass
            elif attr == "csrfmiddlewaretoken":
                pass
            else:
                print "%s=%s" % (attr,request.POST[attr])
                
                if request.POST[attr]=="clear" or request.POST[attr]=="":
                    return render_to_response(
                                    'quiz/incomplete.html',
                                    {},
                                    context_instance = RequestContext(request),)
                    
                """Get a question object for our current form params"""
                qtion=Question.objects.get(slug=attr)
                """Get an answer object for our current form params"""
                a=Answer.objects.get(answer=request.POST[attr])
                
                if (request.POST[attr]==a.answer) and (a.correct==True):
                    """User provided correct answer"""
                    correct=True
                else:
                    """User provided incorrect answer"""
                    correct=False
                """Get a response object"""    
                r=Response.objects.get(quiz=quizid, question=qtion)
                r.answer=a
                r.correct=correct
                r.save(force_update=True)
                """Response Updated"""
        
        """Grade the quiz"""
        num_questions=Response.objects.filter(quiz=q).count()
        num_right = Response.objects.filter(quiz=q, correct=True)
        num_right = num_right.count()
        
        """Calculate the score"""    
        score =(float(num_right) / float(num_questions)) * 100

        """write the score to the model object"""
        q.score=score
        q.id=quizid
        q.save(force_update=True)
        
        """grab the questions that the user must get right"""
        must_get_right= Question.objects.filter(must_get_right=True)
        
        """Default passed_required flag to True"""
        passed_required=True

        for mgrq in must_get_right:
            """Iterate through list to see if user missed any"""
            is_response_right = Response.objects.get(quiz=quizid, question=mgrq)

            if is_response_right.correct==False:
                """"The user did not get all the required questions right """
                passed_required=False 
        
        """If both the minimum score was reached AND all must_get_right ?s were right"""
        if score>=MIN_QUIZ_PASS_SCORE and passed_required==True:
            q.passed=True
        
        """Save the quiz"""
        q.id =quizid
        q.save(force_update=True)
        
        """Display the complete screen by redirecting"""
        return HttpResponseRedirect(reverse('quiz_complete',
                                            kwargs={'category': category}))
    
    else:
        """ This is an HTTP GET so let's draw the form"""        
        """Check and see if the user has already passed."""
        try:
            """Quiz already passed"""
            quiz=Quiz.objects.filter(user=request.user, passed=True, category=c)[0]
            passed=True
            form=None
            quizid="foo"
        except(IndexError):
            passed=False
            """The user has not passed so let's generate a quiz."""
            
            """Create a new quiz"""
            newquiz=Quiz(category=c, user=request.user, passed=False)
            newquiz.save()
            quizid=newquiz.id
            """Get the required questions and x random questions."""
            
            """Get the random questions for the quiz"""
            random_questions=Question.objects.filter(always_ask=False, category=c).order_by('?')[:QUIZ_NUM_RAND_QUESTIONS]
            for rq in random_questions:
                """Load the questions into response objects"""
                r=Response(quiz=newquiz, question=rq)
                r.save()
            
            """Get the must ask questions """
            must_ask_questions=Question.objects.filter(always_ask=True)
            
            for maq in must_ask_questions:
                """Load into responses"""
                r=Response(quiz=newquiz, question=maq)
                r.save()
            
            """get all the possible answers and we'll match up Q-to-A in the form gen"""
            answers=Answer.objects.all()
        
            """Create the form with the same info"""
            form = TakeQuizForm(must_ask_questions,random_questions,answers) # An unbound form
            
        data, errors = {}, {}
    
    return render_to_response(
        'quiz/take_quiz.html',
        {'form': form, 'passed':passed, 'quizid':quizid},
        context_instance = RequestContext(request),)
    
    
@login_required
def complete(request, category):
    """
    This view is displayed when a quiz is completed.
    It displays the users grade & what was missed
    """
    if request.method == 'GET':
        #default passed to true and check to see if he/she actually passed
        passed=True
        
        """get the category object from the category name passed on the url."""
        c=get_object_or_404(Category,slug=category)
        
        """Make sure the user has a past quiz to grade/display"""
        q=get_list_or_404(Quiz,user=request.user, category=c)
        
        try:
            q=Quiz.objects.filter(user=request.user, passed=True, category=c).latest()
            score=q.score
        except(Quiz.DoesNotExist):
            passed=False
            try:
                q=Quiz.objects.filter(user=request.user, category=c).latest()
                missed=Response.objects.filter(quiz=q, correct=False)
                score=q.score
            except(Quiz.DoesNotExist):
                score=0
        if q:
            missed = Response.objects.filter(quiz=q, correct=False)
            answers = Answer.objects.all() 
        
        #build a list of dicts containing the right answers
        missedlist=[]
        for m in missed:
            
            rightanswer=Answer.objects.get(question=m.question, correct=True)
            #print m.question.question_text, m.answer, rightanswer
            
            dict={
                  'question_text'   : m.question.question_text,
                  'right_answer'    : rightanswer.answer,
                  'your_answer'     : m.answer.answer,
                  'explanation'     : m.question.explanation
                  }
            
            missedlist.append(dict)
    
        return render_to_response(
            'quiz/complete.html',
            {'passed':passed,
             'score':score,
             'min_quiz_pass_score': MIN_QUIZ_PASS_SCORE,
             'missedlist':missedlist},
            context_instance = RequestContext(request),)
    else:
        """return 405"""
        return HttpResponseNotAllowed("405: Method Not Allowed")

@login_required    
def dashboard(request):
    """Display a quiz dashboard to admins only"""

    if request.user.is_staff==False:
        """return 403"""
        return HttpResponseForbidden("403: Forbidden")
     
    if request.method == 'GET':
        """TOTALS------------------------------------------"""
        
        """How many people have passed v/s taken the test?"""
        number_of_tries = len(Quiz.objects.filter(score__gt=-1))
        number_of_passed = len(Quiz.objects.filter(passed=True))
        """Only if report number_of_tries if != divide by zero"""
        if number_of_tries>0 and number_of_passed>0:
            pass_fail_ratio =  float(number_of_passed) / float(number_of_tries)
            pass_fail_ratio = round(pass_fail_ratio,2)
        else:
            pass_fail_ratio = "Unavailable"
        
        """Average number of tries per user"""        
        """Get all the users who are not staff or admin"""
        num_users=Quiz.objects.filter(score__gt=-1).aggregate(num_users=Count('user', distinct=True))
        num_users=num_users['num_users']
        
        num_tries = len(Quiz.objects.filter(score__gt=-1))
        
        """Only if report average_num_tries if != divide by zero"""
        if num_users>0 and num_tries>0:
            average_num_tries= float(num_tries)/float(num_users)
        else:
            average_num_tries= "Unavailable"
        
        
        """Average score"""
        average_score = Quiz.objects.filter(score__gt=-1).aggregate(Avg('score'))
        average_score = average_score['score__avg']
        if average_score:
            average_score = round(average_score,1)
        else:
            average_score=0.0
            
        """Average Passing Score"""
        average_passing_score = Quiz.objects.filter(score__gt=-1, passed=True).aggregate(Avg('score'))
        average_passing_score = average_passing_score['score__avg']
        if average_passing_score:
            average_passing_score =round(average_passing_score, 1)
        else:
            average_passing_score = 0.0
        
        
        """BY CATEGORY------------------------------------------"""    
        """Average Score by Category"""      
        average_score_by_category = Category.objects.filter(
                quiz__score__gt=-1).annotate(avg_score=Avg('quiz__score'))

        
        """Average Passing Score by Category"""
        average_passing_score_by_category = Category.objects.filter(quiz__score__gt=-1,
                    quiz__passed=True).annotate(avg_score=Avg('quiz__score'))
        
        return render_to_response(
            'quiz/dashboard.html',
            {
            'number_of_tries':                    number_of_tries,
            'number_of_passed':                   number_of_passed,
            'num_users':                          num_users,
            'pass_fail_ratio':                    pass_fail_ratio,
            'average_num_tries':                  average_num_tries,
            'average_score':                      average_score,
            'average_passing_score':              average_passing_score,
            'average_score_by_category':          average_score_by_category,
            'average_passing_score_by_category':  average_passing_score_by_category,
            'min_quiz_pass_score':                MIN_QUIZ_PASS_SCORE,
             },
            context_instance = RequestContext(request),)
    else:
        """return 405"""
        return HttpResponseNotAllowed("405: Method Not Allowed")
