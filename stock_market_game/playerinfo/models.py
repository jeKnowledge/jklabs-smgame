from django.contrib.auth.models import User, UserManager
from django.db import models
from django import forms

# Create your models here.

class UserCredit(models.Model):
	user=models.OneToOneField(User, primary_key=True)
	current_credits=models.IntegerField()
	
	objects=UserManager()
	
	def debit(self,value):
		self.current_credits=self.current_credits-value
	
	def credit(self,value):
		self.current_credits=self.current_credits+value

class PrivateMessage(models.Model):
	sender=models.ForeignKey(User, related_name='+')
	receiver=models.ForeignKey(User, related_name='+')
	send_date=models.DateTimeField()
	content=models.TextField()
		
class Award(models.Model):
	title=models.CharField(max_length=128)
	winner=models.ForeignKey(User)
	creation_date=models.DateTimeField(blank=True, null=True)
	badge=models.CharField(max_length=128)
	
class MessageForm(forms.Form):
	player_to=forms.CharField(max_length=128)
	mcontent=forms.CharField()
	
	
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend


def facebook_extra_values(sender,user, response, details, **kwargs):
	return False
	
pre_update.connect(facebook_extra_values, sender=FacebookBackend)
