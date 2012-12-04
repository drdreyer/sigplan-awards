from django import forms
from django.contrib.auth.models import User

from models import *

class NominatorForm(forms.ModelForm):
    class Meta:
        model = Nominator
        exclude = ('verified','web_key','created_date',)
        
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ('nominator','created_date',)
        
class SupporterForm(forms.ModelForm):
    class Meta:
        model = Supporter
        exclude = ('candidate','web_key','created_date',)
        
class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        widgets = {
            'name': forms.TextInput(attrs={'size':'70'}),
            'link': forms.TextInput(attrs={'size':'70'}),
            'email_title': forms.TextInput(attrs={'size':'70'}),
            'email': forms.TextInput(attrs={'size':'70'}),
            'award_text': forms.Textarea(attrs={'rows':20, 'cols':70}),
        }

class PendingCommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = PendingCommitteeMember
        exclude = ('award','web_key',)
    
class ActivateCommitteeMemberForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=30, min_length=4)
    email = forms.EmailField()
    password = forms.CharField(max_length=16, min_length=6,widget=forms.PasswordInput(render_value=False))
    password_again = forms.CharField(max_length=16, min_length=6,widget=forms.PasswordInput(render_value=False))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if ' ' in username:
            raise forms.ValidationError(u'Username must not contain spaces')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s already exists' % username )
    
    def clean_password_again(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_again')
    
        print '%s %s' % (password1, password2)
    
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2    
    
    