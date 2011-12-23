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
        
    #fetch total freggies -----------------------------------------------------
    
    freggies=Freggie.objects.filter(user=request.user).count()
    
    return render_to_response('roulette/index.html',
            {
             'last_spin_date':last_spin_date(request.user),
             'can_spin':can_spin(request.user),
            },
            context_instance = RequestContext(request),)