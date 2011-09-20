from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
	active=models.BooleanField()
	name=models.CharField(max_length=128)
	website=models.URLField()
	foundation=models.DateField()
	about=models.TextField()
	
	shares=models.IntegerField()
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
	player_from=models.ForeignKey(User, related_name='+')
	

class GEvent(models.Model):
	e_type=models.CharField(max_length=12)
	player_from=models.ForeignKey(User, related_name='+')
	player_to=models.ForeignKey(User, related_name='+')
	company=models.ForeignKey(Company, related_name='+')
	e_value=models.IntegerField()
	#Incomplete
	
	#here goes the methos over these objects
	

class MenuItem(models.Model):
	menu_name=models.CharField(max_length=12)
	link_name=models.CharField(max_length=30)
	link_url=models.URLField()
