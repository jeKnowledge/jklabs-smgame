from gamepress.models import Article, Comment
from django.contrib import admin

#Configurations of how the objects and their properties should be shown



#The models that should be appear in the admin interface
admin.site.register(Article)
admin.site.register(Comment)

