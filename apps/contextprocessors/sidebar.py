#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db.models import Sum
from ..checkin.models import Freggie, Comment, BadgePoints
from ..questions.models import CorrectAnswerPoints
from ..roulette.models import Roulette
from ..tips.models import CurrentTip, Tip

def sidebar(request):
    '''
    A context processor to add the "sidebar" content to every page
    '''
    
    #get the current tip
    try:
        ct=CurrentTip.objects.get(pk=1)
        t=Tip.objects.get(pk=ct.index)
        tip_text=t.text
    except(Tip.DoesNotExist):
        tip_text="No tip to display"
    except(CurrentTip.DoesNotExist):
        tip_text="No tip to display"
    except:
        tip_text="No tip to display"
    
    
    #fetch points
    
    try:
        freggie_points = Freggie.objects.filter(user=request.user).aggregate(Sum('points'))
        if freggie_points['points__sum']== None:
            freggie_points['points__sum']=0

        badge_points = BadgePoints.objects.filter(user=request.user).aggregate(Sum('points'))
        if badge_points['points__sum']== None:
            badge_points['points__sum']=0
        
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
                roulette_points['points__sum'] + question_points['points__sum'] + \
                badge_points['points__sum']

        freggie_points  = freggie_points['points__sum']
        comment_points  = comment_points['points__sum']
        roulette_points = roulette_points['points__sum']
        question_points = question_points['points__sum']
        badge_points    = badge_points['points__sum']
    
        if points>=10:
            wager_points_range=range(10,points+1)
        else:
            wager_points_range=[]
    except:
        return {'freggie_points': 0,
                'comment_points': 0,
                'roulette_points': 0,
                'question_points': 0, 
                'points': 0,
                'badge_points':0,
                'tip_text':tip_text,
                'wager_points_range': [0,],}
        
    return {'freggie_points': freggie_points,
             'comment_points': comment_points,
            'roulette_points': roulette_points,
            'question_points': question_points,
            'badge_points':badge_points,
             'points': points,
             'tip_text':tip_text,
             'wager_points_range': wager_points_range,}
    
    
   