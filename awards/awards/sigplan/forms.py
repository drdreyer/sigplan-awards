from django.forms import Form, ModelForm

from models import *

class NominatorForm(ModelForm):
    class Meta:
        model = Nominator
        exclude = ('verified','web_key','created_date',)
        
class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        exclude = ('nominator','created_date',)
        
class SupporterForm(ModelForm):
    class Meta:
        model = Supporter
        exclude = ('candidate','web_key','created_date',)
        
        
        
        