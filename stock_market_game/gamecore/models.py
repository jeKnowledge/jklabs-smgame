from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
	'''
		Model of the objects representing one company.
	'''
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
	'''
		Each User may have many investments in diferent companies. 
		each object from this model represents the cake of all shares of 
		1 User from 1 company.
	'''
	owner=models.ForeignKey(User)
	of_company=models.ForeignKey(Company)
	n_shares=models.IntegerField()
	initial_value=models.FloatField()
	
	#here goes the methos over these objects
	
class Proposal(models.Model):
	'''
		If a user wants to buy or sell shares he creates a proposal.
		This info will be shared with the other users
	'''
	p_type=models.CharField(max_length=12)
	shares=models.IntegerField()
	per_share=models.IntegerField()
	player_from=models.ForeignKey(User, related_name='+')
	company=models.ForeignKey(Company, related_name='+')
	

class GEvent(models.Model):
	'''
		Info About the diferent events ocurring in the game
		Represents the historical data of the game. The data and calculations 
		about the market activity are made with this objects
	'''
	e_type=models.CharField(max_length=12)
	player_from=models.ForeignKey(User, related_name='+')
	player_to=models.ForeignKey(User, related_name='+')
	company=models.ForeignKey(Company, related_name='+')
	amount_of_shares=models.IntegerField()
	total_credits=models.IntegerField()
	event_date=models.DateField()
	#Incomplete
	
	#here goes the methos over these objects

class EventComment(models.Model):
	'''
		Each event may have many comments.
	'''
	author=models.ForeignKey(User, related_name='+')
	event=models.ForeignKey(GEvent)
	posted=models.DateTimeField()
	content=models.TextField()
	

class MenuItem(models.Model):
	'''
		Info about each menu entry
	'''
	menu_name=models.CharField(max_length=20)
	link_name=models.CharField(max_length=30)
	link_url=models.CharField(max_length=30)


#Below you can find all the forms used by core functions

class TradeForm(forms.Form):
	'''
		Form used to buy and Sell shares
	'''
	value=forms.FloatField()
	shares=forms.IntegerField()
	
class CommentForm(forms.Form):
	'''
		From used to retrieve content for the comments in
		the events
	'''
	content=forms.CharField()
