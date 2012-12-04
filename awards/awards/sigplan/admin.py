from django.contrib import admin
from django.forms import TextInput, Textarea

from awards.sigplan.models import *

class AwardModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'70'})},
        models.TextField: {'widget': Textarea(attrs={'rows':20, 'cols':70})},
    }
    
admin.site.register(Award, AwardModelAdmin)
admin.site.register(Czar)
admin.site.register(CommitteeMember)
admin.site.register(PendingCommitteeMember)
admin.site.register(Nominator)
admin.site.register(Candidate)
admin.site.register(Supporter)