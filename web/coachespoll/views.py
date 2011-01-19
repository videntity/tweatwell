from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from tweatwell.web.coachespoll.models import MaleCoachesPoll, FemaleCoachesPoll


@login_required
def coaches(request):
    mcp=MaleCoachesPoll.objects.all()
    mcplength=len(mcp)
    fcp=FemaleCoachesPoll.objects.all()
    fcplength=len(fcp)

    return render_to_response(
            'rankings/coaches.html',
            {
            'mcp': mcp,
            'mcplength': mcplength,
            'fcp': fcp,
            'fcplength': fcplength,
             },
            context_instance = RequestContext(request),)
