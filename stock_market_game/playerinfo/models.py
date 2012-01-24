from django.contrib.auth.models import User, UserManager
from django.db import models
from django import forms

# Create your models here.

class UserCredit(models.Model):
	''' 
		This object is created of each new user that logs in the game.
		It adds to the user info about his current credits.
	'''
	user=models.OneToOneField(User, primary_key=True)
	current_credits=models.IntegerField()
	
	objects=UserManager()
	
	def debit(self,value):
		'''
			removes "value" credits from the user account
		'''
		self.current_credits=self.current_credits-value
	
	def credit(self,value):
		'''
			adds "value" credits to the user account
		'''
		self.current_credits=self.current_credits+value

class PrivateMessage(models.Model):
	'''
		This model represents one message private message sent.
		It has one date, 2 users (one sender and one receiver) and the content of the message.
	'''
	sender=models.ForeignKey(User, related_name='+')
	receiver=models.ForeignKey(User, related_name='+')
	send_date=models.DateTimeField()
	content=models.TextField()
		
class Award(models.Model):
	'''
		This model represents one Award or Achievement by the user.
		It includes the "title" won, the "winner", the date it was won ("creation_date") and
		the url for the badge to show on the profile
	'''
	title=models.CharField(max_length=128)
	winner=models.ForeignKey(User)
	creation_date=models.DateTimeField(blank=True, null=True)
	badge=models.CharField(max_length=128)
	
class MessageForm(forms.Form):
	'''
		Form used to receive the private message content, 
		before it creates a provate message. 
	'''
	player_to=forms.CharField(max_length=128)
	mcontent=forms.CharField()
	


#Just some code that the "SocialAuth" App needs. 
#TODO needs a better documentation
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend


def facebook_extra_values(sender,user, response, details, **kwargs):
	return False
	
pre_update.connect(facebook_extra_values, sender=FacebookBackend)
