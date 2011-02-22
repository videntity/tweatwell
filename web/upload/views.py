from django.http import HttpResponse, Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from tweatwell import settings
from tweatwell.web.utils import handle_uploaded_file, uploadFile2RESTCat, query_restcat, sendmail_for_comment
from tweatwell.web.upload.forms import *
import datetime, os, sys, types
import pycurl
from omhe.core.parseomhe import parseomhe

@login_required
def upload_file(request,user):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path=handle_uploaded_file(request.FILES['file'], request.user)
            if file_path:
                tx=uploadFile2RESTCat(request, file_path)
                
                return render_to_response('upload/upload_success.html', {'tx': tx, 'file_path': file_path},
                              context_instance = RequestContext(request),)
            else:
                return HttpResponseRedirect(reverse('file_upload_failure'))
    else:
        form = UploadFileForm()
    return render_to_response('web/upload_file.html', {'form': form},
                              context_instance = RequestContext(request),)

@login_required
def upload_file_success(request):
    return render_to_response('upload/upload_success.html',
                              context_instance = RequestContext(request),)

@login_required
def upload_bp(request, user):
    if request.method == 'POST':
        form = BPUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('stats_bp',
                                            kwargs={'user': user}))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = BPUploadForm()
    return render_to_response('upload/bp.html', {'form': form},
                              context_instance = RequestContext(request),)
    
@login_required
def upload_wt(request, user):
    if request.method == 'POST':
        form = WTUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            
            if code==200:
                return HttpResponseRedirect(reverse('stats_wt',
                                            kwargs={'user': user}))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = WTUploadForm()
    return render_to_response('upload/wt.html', {'form': form},
                              context_instance = RequestContext(request),)



@login_required
def upload_omhe(request, user):
    if request.method == 'POST':
        form = OMHEUploadForm(request.POST)
        if form.is_valid():            
            try:
                responsedict=form.save(user)
                if responsedict['code']==200:
                    
                    return HttpResponseRedirect(reverse('home_index'))
                else:
                    return HttpResponseRedirect(reverse('upload_error',
                                                kwargs={'code': responsedict['code']}))
                    
            except(KeyError):
                return HttpResponseRedirect(reverse('home_index_error',
                                            kwargs={'error': "Oops! I didn't understand that."}))
    else:
        form = OMHEUploadForm()
    return render_to_response('upload/texti.html', {'form': form},
                              context_instance = RequestContext(request),)





@login_required
def upload_wt_ajax(request, user):
    if not request.is_ajax():
        pass
        #msg="Fobbidden"
        #return HttpResponse(msg, status=401)
    if request.method == 'POST':
        form = AJAXWTUploadForm(request.POST)
        
        if form.is_valid():            
            responsedict=form.save(user)
            if responsedict['code']==200:
                return HttpResponse(responsedict['body'],
                                    mimetype="application/json",
                                    content_type='application/json',
                                    status=200)
            else:
                #print "Weight Update Failed." % (code)
                msg="Weight Update Failed." % (code)
                return HttpResponse(msg, status=code)
        else:
            msg="The form was invalid"
            return HttpResponse(msg, status=400)
            
    return render_to_response('upload/wt.html', {'form': form},
                              context_instance = RequestContext(request),)



@login_required
def upload_omhe_ajax(request, user):
    print "here"
    if not request.is_ajax():
        print "not AJAX"
        return HttpResponse("OK", status=200)
    else:
        print "Hello AJAX"
        #return HttpResponse(msg, status=401)

        return HttpResponse("OK", status=200)
            
@login_required
def upload_ci_ajax(request, user):
    
    if not request.is_ajax():
        msg="Fobbidden"
        return HttpResponse(msg, status=401)
    if request.method == 'POST':
        form = AJAXCIUploadForm(request.POST)

        if form.is_valid():            
            
            responsedict=form.save(user)
            if responsedict['code']==200:
                return HttpResponse(responsedict['body'],
                                    mimetype="text/plain",
                                    content_type='text/plain',
                                    status=200)
            else:
                return HttpResponse(responsedict['body'], status=code)
        else:
            msg="The form was invalid"
            return HttpResponse(msg, status=400)
            
    return render_to_response('upload/ci.html', {'form': form},
                              context_instance = RequestContext(request),)





@login_required
def upload_ffm(request, user):
    if request.method == 'POST':
        form = FFMUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('home_index'))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = FFMUploadForm()
    return render_to_response('upload/ffm.html', {'form': form},
                              context_instance = RequestContext(request),)
    
    
@login_required
def upload_fm(request, user):
    if request.method == 'POST':
        form = FMUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('home_index'))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = FMUploadForm()
    return render_to_response('upload/fm.html', {'form': form},
                              context_instance = RequestContext(request),)


@login_required
def upload_comment(request, user):
    if request.method == 'POST':
        form = CommentUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                ## print request.POST['idr'],  "Send an email to the person who's status was commented upon"
                sendmail_for_comment(request.user.username, request.POST['ci'], request.POST['idr'])
                return HttpResponseRedirect(reverse('home_index'))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = CommentUploadForm()
    return render_to_response('upload/comment.html', {'form': form},
                              context_instance = RequestContext(request),)

    
@login_required
def upload_pbf(request, user):
    if request.method == 'POST':
        form = PBFUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('home_index'))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = PBFUploadForm()
    return render_to_response('upload/pbf.html', {'form': form},
                              context_instance = RequestContext(request),)
    
@login_required
def upload_ci(request, user):
    if request.method == 'POST':
        form = CIUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('twhome_index'))
            else:
                return HttpResponseRedirect(reverse('twhome_index'))
    else:
        form = CIUploadForm()
    return render_to_response('upload/ci.html', {'form': form},
                              context_instance = RequestContext(request),)


@login_required
def upload_texti(request, user, omheprefix):
    if request.method == 'POST':
        form = TextiUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user, omheprefix)
            if code==200:
                return HttpResponseRedirect(reverse('twhome_index'))
            else:
                return HttpResponseRedirect(reverse('twhome_index'))
    else:
        form = TextiUploadForm()
    return render_to_response('upload/texti.html', {'form': form},
                              context_instance = RequestContext(request),)



   
@login_required
def upload_st(request, user):
    if request.method == 'POST':
        form = STUploadForm(request.POST)
        if form.is_valid():            
            code=form.save(user)
            if code==200:
                return HttpResponseRedirect(reverse('stats_st',
                                            kwargs={'user': user}))
            else:
                return HttpResponseRedirect(reverse('upload_error',
                                            kwargs={'code': code}))
    else:
        form = STUploadForm()
    return render_to_response('upload/st.html', {'form': form},
                              context_instance = RequestContext(request),)
    
    
    
def upload_error(request, code):
    return render_to_response('upload/error.html', {'code': code},
                              context_instance = RequestContext(request),)



    
