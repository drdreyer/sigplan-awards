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
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.loader import render_to_string
from django.template import Context, loader, RequestContext
from django.views.decorators.http import require_POST


from forms import *

def index(request):
    awards = Award.objects.all()
    return render(request, 'index.html', { 
      'awards':awards
      })

@login_required
def manage(request):
    if request.user.is_authenticated():
        czars = Czar.objects.filter(user__exact=request.user)
        members = CommitteeMember.objects.filter(user__exact=request.user)

        num_committees = len(czars) + len(members)
        if num_committees > 1:
            return multiple_committees(request, czars, members)

        if num_committees == 1:
            if len(czars) == 1:
                return czar_index(request, czars[0])
            if len(members) == 1:
                return committee_index(request, members[0])


@login_required
def multiple_committees(request, czars, members):
    return render(request, 'multiple.html', {
        'czars':czars,
        'members':members,                                  
        })


@login_required
def award_member(request, award_id):
    try:
        czar = Czar.objects.get(user__exact=request.user, award__id=award_id)
        return czar_index(request, czar)
    except:
        pass
    
    try:
        member = CommitteeMember.objects.get(user__exact=request.user, award__id=award_id)
        return committee_index(request, member)
    except:
        pass
    
    raise Http404
    
@login_required
def czar_index(request, czar):
    if czar.user == request.user:
        return committee_index_helper(request, czar, 'czar.html')
    raise Http404
    
@login_required
def committee_index(request, member):
    if member.user == request.user:
        return committee_index_helper(request, member, 'committee.html')
    raise Http404
    
def committee_index_helper(request, member, template):
    award = member.award
    czars = Czar.objects.filter(award=award)
    members = CommitteeMember.objects.filter(award=award)
    pendings = PendingCommitteeMember.objects.filter(award=award)
    candidates = Candidate.objects.filter(award=award).order_by('-nominator__verified', 'created_date')

    return render(request, template, { 
        'request':request,
        'award':award,
        'czars':czars,
        'members':members,
        'pendings':pendings,
        'candidates':candidates,
        })
    
@login_required
def edit_award(request, award_id):
    award = Award.objects.get(id=award_id)
    czar = Czar.objects.get(user__exact=request.user, award=award)

    if czar.award == award:
        if request.method == 'POST': # If the form has been submitted...
            form = AwardForm(request.POST, instance=award) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                form.save();
                return HttpResponseRedirect('/') # Redirect after POST
        else:
            form = AwardForm(instance=award) # An unbound form

        return render_to_response('edit_award.html', { 
            'request':request,
            'award':award,
            'form':form,
            },context_instance=RequestContext(request))
        return HttpResponse("Edit Award %s" % award)
        
    raise Http404

@login_required
def add_committee_member(request, award_id):
    award = Award.objects.get(id=award_id)
    czar = Czar.objects.get(user__exact=request.user, award=award)

    if czar.award == award:
        if request.method == 'POST': # If the form has been submitted...
            form = PendingCommitteeMemberForm(request.POST) # A form bound to the POST data
            form.instance.award = award
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                form.save();
                email_pending_member(czar, form.instance)
                form = PendingCommitteeMemberForm();
        else:
            form = PendingCommitteeMemberForm() # An unbound form

        czars = Czar.objects.filter(award=award)
        members = CommitteeMember.objects.filter(award=award)
        pendings = PendingCommitteeMember.objects.filter(award=award)

        print pendings

        return render_to_response('add_committee_member.html', { 
            'request':request,
            'award':award,
            'form':form,
            'czars':czars,
            'members':members,
            'pendings':pendings,
            },context_instance=RequestContext(request))
        
    raise Http404

def activate_committee_member(request, web_key):
    try:
        pending = PendingCommitteeMember.objects.get(web_key=web_key)
        
        if request.user.is_authenticated():
            CommitteeMember.objects.create(user=request.user,award=pending.award)
            pending.delete()
            return HttpResponseRedirect('/')
        
        if request.method == 'POST': # If the form has been submitted...
            form = ActivateCommitteeMemberForm(request.POST) # A form bound to the POST data
            
#            form.instance.award = award
            if form.is_valid(): # All validation rules pass
                user = User.objects.create_user(
                                username=form.cleaned_data['username'], 
                                email=form.cleaned_data['email'], 
                                password=form.cleaned_data['password'])
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])
                login(request, user)
                CommitteeMember.objects.create(user=user,award=pending.award)
                pending.delete()
                
                return HttpResponseRedirect('/')
        else:
            (first_name,foo,last_name) = pending.name.partition(' ')
            form = ActivateCommitteeMemberForm(initial={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': pending.email,
                    })
        
        return render_to_response('activate_committee_member.html', { 
                'form':form,
                'pending':pending,
                'help_email': pending.award.email,
            },context_instance=RequestContext(request))
        
    except PendingCommitteeMember.DoesNotExist:
        raise Http404

def email_pending_member(czar, pending):
    message = render_to_string('new_committee_member_email.txt',
                                       { 'pcm': pending,
                                         'award': czar.award,
                                         'czar': czar, 
                                         'site_name': Site.objects.get_current()
                                        })
    
    send_mail('Welcome to the %s awards committee.' % pending.award.name, message, czar.award.email_title+'<'+czar.award.email+'>',
        [pending.name+'<'+pending.email+'>'], fail_silently=False)
    
    
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

@login_required
def make_czar(request, award_id, member_id):
    try:
        award = Award.objects.get(id=award_id)
        current_czar = Czar.objects.get(award=award,user=request.user)
        member = CommitteeMember.objects.get(id=member_id)
        
        if request.GET.get('confirm', 'false') == 'true':

            CommitteeMember.objects.create(user=request.user,award=award)
            Czar.objects.create(user=member.user,award=award)
            
            current_czar.delete()
            member.delete()
            
            return HttpResponseRedirect('/')
        
        return render_to_response('make_czar.html', 
                              {
                                'award':award,
                                'current_czar':current_czar,
                                'member':member,
                               },
                              context_instance=RequestContext(request))
        
    except (Award.DoesNotExist, CommitteeMember.DoesNotExist, Czar.DoesNotExist):
        raise Http404
    
    

def nominate(request, award_name):
    award = Award.objects.get(short_name=award_name)
    forms = []
    valid = True
    if request.method == 'POST': # If the form has been submitted...
        
        print request.POST.items()
        
        
        c_form = CandidateForm(request.POST, prefix='candidate') 
        form = c_form
        form.form_title = "Candidate's Information"
        if not form.is_valid(): # All validation rules pass
            valid = False
        forms.append(form)
        
        n_form = NominatorForm(request.POST, prefix='nominator') 
        form = n_form
        form.form_title = "Your Contact Information"
        if not form.is_valid(): # All validation rules pass
            valid = False
        forms.append(form)

        valid_supporter_forms = []        
        for index in range(1,11):
            prefix = 'supporter-%s' % index
            form = SupporterForm(request.POST, prefix=prefix)
            form.form_title = "Supporter %s" % index
            
            if index <= 5 or request.POST[prefix+'-name'] or request.POST[prefix+'-email']:
                if form.is_valid(): # All validation rules pass
                    valid_supporter_forms.append(form)
                else:
                    valid = False
            else:
                form.dont_show_errors = True
                if index > 5:
                    form.hidden = True

            forms.append(form)            
            
        if valid:
            if "confirm" in request.POST:
                nominator = n_form.save()
                c_form.instance.nominator = nominator
                c_form.instance.award = award
                candidate = c_form.save()

                for s_form in valid_supporter_forms:
                    s_form.instance.candidate = candidate
                    s_form.save()

                email_nominator(nominator, candidate)
                return HttpResponseRedirect('/thank_nominator/') # Redirect after POST

            if "nominate" in request.POST:
                return render(request, 'verify_nomination.html', {
                    'forms': forms,
                    'award': award,
                })
            
    else:
        form = CandidateForm(prefix='candidate')
        form.form_title = "Candidate's Information"
        forms.append(form)
        
        form = NominatorForm(prefix='nominator')
        form.form_title = "Your Contact Information"
        forms.append(form)
        
        for index in range(1,11):
            form = SupporterForm(prefix='supporter-%s' % index)
            form.form_title = "Supporter %s" % index
            if index > 5:
                form.hidden = True
            forms.append(form)            
            
    return render(request, 'nominate.html', {
        'forms': forms,
        'award': award,
        'errors': not valid,
    })

def email_nominator(nominator, candidate):
    award = candidate.award
    czar = Czar.objects.filter(award=award)[0]
    supporters = Supporter.objects.filter(candidate=candidate)
 
    message = render_to_string('complete_nomination_email.txt',
                                   { 'nominator': nominator,
                                     'candidate': candidate,
                                     'award': award,
                                     'czar': czar, 
                                     'supporters': supporters,
                                     'site_name': Site.objects.get_current(),
                                    })

    send_mail('SIGPLAN %s award nomination for %s' % (award.name,candidate.name), message, award.email_title+'<'+award.email+'>',
        [nominator.name+'<'+nominator.email+'>'], fail_silently=False)
      
def thank_nominator(request):
    return render(request, 'thank_nominator.html')

def complete_nomination(request, web_key):
    try:
        nominator = Nominator.objects.get(web_key=web_key)
        nominator.verified = True
        nominator.save()
        
        return render(request, 'thank_nominator2.html')
    except Nominator.DoesNotExist:
        raise Http404

@login_required        
def candidate(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
    
        is_czar = False    
        is_committee = False
        try:
            Czar.objects.get(user__exact=request.user,award=candidate.award)
            is_czar = True
        except Czar.DoesNotExist:
            try:
                CommitteeMember.objects.get(user__exact=request.user,award=candidate.award)
                is_committee = True
            except:
                raise Http404


        if is_czar or is_committee:            
            supporters = Supporter.objects.filter(candidate=candidate)
            can_request_all = False
            
            for supporter in supporters:
                if not supporter.statement:
                    can_request_all = True
            
            return render(request, 'candidate.html', {
                'candidate': candidate,
                'supporters': supporters,
                'is_czar': is_czar,
                'can_request_all': can_request_all,
            })

    except Candidate.DoesNotExist:
        raise Http404
    
@login_required        
def email_supporter(request, supporter_id):
    try:
        supporter = Supporter.objects.get(id=supporter_id)
    
        try:
            Czar.objects.get(user__exact=request.user,award=supporter.candidate.award)
            do_email_supporter(supporter)
            return HttpResponseRedirect('/candidate/%s/' % supporter.candidate.id)
        except Czar.DoesNotExist:
            raise Http404
    except Supporter.DoesNotExist:
        raise Http404

@login_required        
def email_supporters(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        
        try:
            Czar.objects.get(user__exact=request.user,award=candidate.award)

            supporters = Supporter.objects.filter(candidate=candidate)
            
            for supporter in supporters:
                if not supporter.statement:
                    do_email_supporter(supporter)
                
            return HttpResponseRedirect('/candidate/%s/' % candidate_id)
        except Czar.DoesNotExist:
            raise Http404
    except Candidate.DoesNotExist:
        raise Http404
    
    
def do_email_supporter(supporter):
    award = supporter.candidate.award
    czar = Czar.objects.filter(award=award)[0]
    
    message = render_to_string('request_supporter_statement_email.txt',
                                   { 'supporter': supporter,
                                     'award': award,
                                     'czar': czar, 
                                     'site_name': Site.objects.get_current()
                                    })

    to_addr = supporter.name+'<'+supporter.email+'>'
    if supporter.title:
        to_addr = supporter.title+' '+supporter.name+'<'+supporter.email+'>'

#    print to_addr
#    print message
#    return

    send_mail('SIGPLAN %s award nomination for %s' % (award.name,supporter.candidate.name), message, award.email_title+'<'+award.email+'>',
        [to_addr], fail_silently=False)
    supporter.requested = True
    supporter.save()
    

def support_letter(request, web_key):
    try:
        supporter = Supporter.objects.get(web_key=web_key)
    
        if request.method == 'POST': # If the form has been submitted...
            form = SupportStatementForm(request.POST) # A form bound to the POST data
            
#            form.instance.award = award
            if form.is_valid(): # All validation rules pass
                supporter.statement = form.cleaned_data['statement']
                supporter.save()
                return render(request, 'thank_supporter.html')
        else:
            form = SupportStatementForm()
        
        return render_to_response('support_letter.html', { 
                'form':form,
                'supporter':supporter,
                'award':supporter.candidate.award,
                'help_email': supporter.candidate.award.email,
            },context_instance=RequestContext(request))
        
    except Supporter.DoesNotExist:
        raise Http404
    
    
    
