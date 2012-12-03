from django.db import models
import django.contrib.auth.models as auth_models
from django.conf import settings

import random
import sha

class Award(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

# ***************** Roles *******************
class Czar(models.Model):
    user = models.ForeignKey(auth_models.User)
    award = models.ForeignKey(Award)
    created_date = models.DateTimeField('Created', auto_now_add=True)
    
class CommitteeMember(models.Model):
    user = models.ForeignKey(auth_models.User)
    award = models.ForeignKey(Award)
    created_date = models.DateTimeField('Created', auto_now_add=True)
    
class Nominator(models.Model):
    name = models.CharField(max_length=200)  
    affiliation = models.CharField(max_length=200)  
    phone = models.CharField(max_length=200)  
    email = models.CharField(max_length=200)  
    verified = models.BooleanField(default=False) # if the email address has been properly responded to
    web_key = models.CharField(max_length=40, blank=True) # magic link
    created_date = models.DateTimeField('Created', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.web_key:
            self.web_key = sha.new(settings.SECRET_HASH+self.email+str(random.random())).hexdigest()
        super(Nominator, self).save(*args, **kwargs)

class Candidate(models.Model):
    name = models.CharField(max_length=200)  
    award = models.ForeignKey(Award)
    nominator = models.ForeignKey(Nominator)
    affiliation = models.CharField(max_length=200)  
    phone = models.CharField(max_length=200)  
    email = models.CharField(max_length=200)  
    statement = models.TextField(editable=False)
    created_date = models.DateTimeField('Created', auto_now_add=True)
    
class Supporter(models.Model):
    candidate = models.ForeignKey(Candidate)
    name = models.CharField(max_length=200)  
    title = models.CharField(max_length=100) # Mr. Dr. Etc  
    email = models.CharField(max_length=200)  
    statement = models.TextField(editable=False, blank=True)
    web_key = models.CharField(max_length=40, blank=True) # magic link
    created_date = models.DateTimeField('Created', auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.web_key:
            self.web_key = sha.new(settings.SECRET_HASH+self.email+str(random.random())).hexdigest()
        super(Supporter, self).save(*args, **kwargs)

    