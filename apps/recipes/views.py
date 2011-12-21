#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime, os, pycurl, StringIO, json, types, sys
from models import Recipe, RecipeComment
from forms import CommentForm


def recipe(request):
    recipes = Recipe.objects.all()
    
    recipelist=[]
    for r in recipes:
        c=RecipeComment.objects.filter(recipe=r)
        recipeitem = {'recipe': r, 'comments':c}
        recipelist.append(recipeitem)
    

    return render_to_response('recipes/index.html',
                {
                'commentform': CommentForm(),
                'recipelist': recipelist,
                },
            context_instance = RequestContext(request),)

@login_required
def recipe_comment(request, recipe_id):
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if request.method == 'POST':

        form = CommentForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newcomment=form.save(commit=False)
            newcomment.text=data['text']
            newcomment.user=request.user
            newcomment.recipe=recipe
            newcomment.save()
            messages.success(request, "Successfuly added a comment.")
            return HttpResponseRedirect(reverse('recipe'))


