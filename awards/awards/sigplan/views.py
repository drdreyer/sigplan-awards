import datetime
import re
import os
import random
import sha
import logging

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from django.views.decorators.http import require_POST


from forms import *

def index(request):
    return render(request, 'index.html')


    
def sigplan_authenticate(request):
    form = AuthenticationForm()
    errors = ''
    if request.method == 'POST':
#        form = AuthenticationForm(request)
#        if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
#            user = form.get_user()
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next') or '/')
            else:
                # Return a 'disabled account' error message
                #form._errors['username'] = form.error_class(["Account Disabled"])
                errors = 'Account Disabled'
        else:
            # Return an 'invalid login' error message.
            #form._errors['username'] = form.error_class(["Username and password do not match"])
#            form.username.initial = username
            errors = 'Username and Password do not match'
    context = {'form': form }
    if errors:
        context['errors']=errors
    return render_to_response('registration/login.html', 
                              context,
                              context_instance=RequestContext(request))

def profile(request):
    return HttpResponse("Profile")

def nominate(request):
#    if request.method == 'POST': # If the form has been submitted...
#        form = NominateForm(request.POST) # A form bound to the POST data
#        if form.is_valid(): # All validation rules pass
#            # Process the data in form.cleaned_data
#            # ...
#            return HttpResponseRedirect('/thanks/') # Redirect after POST
#    else:
#        form = NominateForm() # An unbound form

    return render(request, 'nominate.html', {
#        'form': form,
    })
    
def czar(request):
    return render(request, 'czar.html', {
#        'form': form,
    })
    