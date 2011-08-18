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
	

class GEvent(models.Model):
	e_type=models.CharField(max_length=12)
	player_from=models.ForeignKey(User, related_name='+')
	player_to=models.ForeignKey(User, related_name='+')
	e_value=models.IntegerField()
	#Incomplete
	
	#here goes the methos over these objects
	
	
