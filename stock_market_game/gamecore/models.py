from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
	active=models.BooleanField()
	name=models.CharField(max_length=128)
	website=models.URLField()
	foundation=models.DateField()
	about=models.TextField()
	
	total_shares=models.IntegerField()
	left_shares=models.IntegerField()
	
	share_value=models.FloatField()
	
	#here goes the methods over these objects
	
	
	
	
class Investment(models.Model):
	owner=models.ForeignKey(User)
	of_company=models.ForeignKey(Company)
	n_shares=models.IntegerField()
	initial_value=models.FloatField()
	
	#here goes the methos over these objects
	
class Proposal(models.Model):
	p_type=models.CharField(max_length=12)
	shares=models.IntegerField()
	per_share=models.IntegerField()
	player_from=models.ForeignKey(User, related_name='+')
	company=models.ForeignKey(Company, related_name='+')
	

class GEvent(models.Model):
	e_type=models.CharField(max_length=12)
	player_from=models.ForeignKey(User, related_name='+')
	player_to=models.ForeignKey(User, related_name='+')
	company=models.ForeignKey(Company, related_name='+')
	amount_of_shares=models.IntegerField()
	total_credits=models.IntegerField()
	event_date=models.DateField()
	#Incomplete
	
	#here goes the methos over these objects
	

class MenuItem(models.Model):
	menu_name=models.CharField(max_length=20)
	link_name=models.CharField(max_length=30)
	link_url=models.CharField(max_length=30)


class TradeForm(forms.Form):
	value=forms.FloatField()
	shares=forms.IntegerField()
	
class ProposalForm(models.forms.ModelForm):
	class Meta:
		model=Proposal
	
