from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	'''
		Model representing one Press Entry. 
		It is composed by 1 title ("atitle"), the content ("acontent")
		and the date ("adate")
	'''
	atitle=models.CharField(max_length=90)
	acontent=models.TextField()
	adate=models.DateTimeField()

class Comment(models.Model):
	'''
		Model of the blog comments. 
		It has the reference for his article ("carticle") and author("cauthor")
		The fields are the content ("ccontent") and date ("cdate").
	'''
	cauthor=models.ForeignKey(User)
	carticle=models.ForeignKey(Article)
	ccontent=models.TextField()
	cdate=models.DateTimeField()
