from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.

class UserCredit(models.Model):
	user=models.OneToOneField(User, primary_key=True)
	current_credits=models.IntegerField()
	
	objects=UserManager()
	
		
class Award(models.Model):
	title=models.CharField(max_length=128)
	winner=models.ForeignKey(User)
	creation_date=models.DateTimeField(blank=True, null=True)
	badge=models.URLField()
	
	
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend


def facebook_extra_values(sender,user, response, details, **kwargs):
	return False
	
pre_update.connect(facebook_extra_values, sender=FacebookBackend)
