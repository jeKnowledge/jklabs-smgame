from playerinfo.models import UserCredit, Award, PrivateMessage
from django.contrib import admin

#Configurations of how the objects and their properties should be shown



#The models that should be appear in the admin interface
admin.site.register(UserCredit)
admin.site.register(Award)
admin.site.register(PrivateMessage)
