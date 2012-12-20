from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from models import *


class TitleInput(forms.TextInput):
    '''
    need some magic javascript and styling to make this work:
.combo-container {
    position: relative;
    height: 18px;
}

.combo-container input {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 999;
    padding: 0;
    margin: 0;
    width: 420px;
}

.combo-select {
    position: absolute;
    top: 0;
    left: 0;
    padding: 0;
    margin: 0;
    width: 438px;
}


$('.combo-select').change(function() {
    $(this).siblings('input').val($(this).children("option").filter(":selected").text());
});
  
    '''
    
    default_options = ["Mrs.","Mr.","Ms.","Dr.","Prof.",]
    
    def render(self, name, value, attrs=None):
        super_def = super(TitleInput, self).render(name,value,attrs)
        selecter = u'<select class="combo-select"><option></option>'
        for option in self.default_options:
            selecter += u'<option>%s</option>' % option            
        selecter += u'</select>'
        return mark_safe(u'<div class="combo-container">%s%s</div>' % (super_def,selecter))
        

class NominatorForm(forms.ModelForm):
    class Meta:
        model = Nominator
        exclude = ('verified','web_key','created_date',)
        
        widgets = {
            'name': forms.TextInput(attrs={'size':'70'}),
            'affiliation': forms.TextInput(attrs={'size':'70'}),
            'email': forms.TextInput(attrs={'size':'70'}),
            'phone': forms.TextInput(attrs={'size':'70'}),
            'award_text': forms.Textarea(attrs={'rows':20, 'cols':70}),
        }
        
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ('award','requested','developers','nominator','created_date',)
        
        widgets = {
            'name': forms.TextInput(attrs={'size':'70'}),
            'affiliation': forms.TextInput(attrs={'size':'70'}),
            'email': forms.TextInput(attrs={'size':'70'}),
            'phone': forms.TextInput(attrs={'size':'70'}),
            'statement': forms.Textarea(attrs={'rows':20, 'cols':70}),
        }

class AwardCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ('award','requested','nominator','affiliation','created_date','email','phone')
        
        widgets = {
            'name': forms.TextInput(attrs={'size':'70'}),
            'statement': forms.Textarea(attrs={'rows':20, 'cols':70}),
            'developers': forms.Textarea(attrs={'rows':20, 'cols':70}),
            'affiliation': forms.TextInput(attrs={'size':'70'}),
        }
        

        
class SupporterForm(forms.ModelForm):
    class Meta:
        model = Supporter
        exclude = ('statement','requested','candidate','web_key','created_date',)
        
        widgets = {
            'title': TitleInput(),
            'name': forms.TextInput(),
            'email': forms.TextInput(),
#            'title': TitleInput(attrs={'size':'70'}),
#            'name': forms.TextInput(attrs={'size':'70'}),
#            'email': forms.TextInput(attrs={'size':'70'}),
        }
        
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
    email = forms.EmailField()
    username = forms.CharField(max_length=30, min_length=4)
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
    
    
class SupportStatementForm(forms.Form):
    statement = forms.CharField( widget=forms.Textarea(attrs={'rows':20, 'cols':70}))

                                  
#class SoftwareAwardAdditionalForm(forms.ModelForm):
#    class Meta:
#        model = SoftwareAwardAdditional
#        exclude = ('candidate',)
#        
#        widgets = {
#            'software_title': forms.TextInput(),
#            'developers': forms.Textarea(attrs={'rows':20, 'cols':70}),
##            'title': TitleInput(attrs={'size':'70'}),
##            'name': forms.TextInput(attrs={'size':'70'}),
##            'email': forms.TextInput(attrs={'size':'70'}),
#        }
