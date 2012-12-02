from django.contrib import admin
from awards.sigplan.models import *

admin.site.register(Award)
admin.site.register(Czar)
admin.site.register(CommitteeMember)
admin.site.register(Nominator)
admin.site.register(Candidate)
admin.site.register(Supporter)