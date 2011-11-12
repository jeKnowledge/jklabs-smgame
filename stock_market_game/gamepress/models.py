from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	atitle=models.CharField(max_length=90)
	acontent=models.TextField()
	adate=models.DateTimeField()

class Comment(models.Model):
	cauthor=models.ForeignKey(User)
	carticle=models.ForeignKey(Article)
	ccontent=models.TextField()
	cdate=models.DateTimeField()
