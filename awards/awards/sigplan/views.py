import datetime
import re
import os
import random
import sha
import logging

from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response, get_object_or_404, render
from django.conf import settings
from django.contrib.auth.models import User

from forms import *

def index(request):
    return HttpResponse("Hello World.")

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