from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import PointsRank


@login_required
def points(request):
    pr=PointsRank.objects.all()
    prlength=len(pr)

    return render_to_response(
            'rankings/points.html',
            {
            'pr': pr,
            'prlength': prlength,
             },
            context_instance = RequestContext(request),)