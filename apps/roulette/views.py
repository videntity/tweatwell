from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from forms import RouletteSpinForm, RouletteJokerForm
from ..checkin.models import Comment, Freggie
from ..questions.models import CorrectAnswerPoints
from models import Roulette, last_spin_date, can_spin
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from ..accounts.models import UserProfile

@csrf_exempt
@login_required
def spin_results(request):
    
    if request.method == 'POST':
        form = RouletteSpinForm(request.POST)
        if form.is_valid():  
            data = form.cleaned_data
            newpoints=form.save(commit=False)
            newpoints.text=data['points']
            newpoints.user=request.user
            newpoints.save()
            return HttpResponse("OK", status=200)
            


@csrf_exempt
@login_required
def joker_results(request):
    
    up=get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = RouletteJokerForm(request.POST)    
        if form.is_valid():  
            data = form.cleaned_data
            #if data['joker_badge']=="true" or data['joker_badge']==True:
            up.joker_badge=True
            up.save()
            return HttpResponse("OK", status=200)

            
@login_required
def roulette_home(request):  
    
    #fetch points
    
    freggie_points = Freggie.objects.filter(user=request.user).aggregate(Sum('points'))
    if freggie_points['points__sum']== None:
        freggie_points['points__sum']=0
    
    comment_points = Comment.objects.filter(user=request.user).aggregate(Sum('points'))
    if comment_points['points__sum']== None:
        comment_points['points__sum']=0    

    roulette_points = Roulette.objects.filter(user=request.user).aggregate(Sum('points'))
    if roulette_points['points__sum']== None:
        roulette_points['points__sum']=0
        
    question_points = CorrectAnswerPoints.objects.filter(user=request.user).aggregate(Sum('points'))
    if question_points['points__sum']== None:
        question_points['points__sum']=0
    
    points = freggie_points['points__sum'] + comment_points['points__sum'] + \
                roulette_points['points__sum'] + question_points['points__sum']

    freggie_points =  freggie_points['points__sum']
    comment_points =  comment_points['points__sum']
    roulette_points =  roulette_points['points__sum']
    question_points = question_points['points__sum']


    if points>=10:
        wager_points_range=range(10,points+1)
    else:
        wager_points_range=[]
        
    
    #fetch total freggies -----------------------------------------------------
    
    freggies=Freggie.objects.filter(user=request.user).count()
    
    return render_to_response('roulette/index.html',
            {
             'freggies': freggies,
             'freggie_points': freggie_points,
             'comment_points': comment_points,
             'roulette_points': roulette_points,         
             'question_points': question_points, 
             'points': points,
             'wager_points_range': wager_points_range,
             'last_spin_date':last_spin_date(request.user),
             'can_spin':can_spin(request.user),
            },
            context_instance = RequestContext(request),)