from django.db import models
from django.conf import settings
from rest_framework.authtoken.serializers import AuthTokenSerializer

#User = settings.AUTH_USER_MODEL
from accounts.models import User

class Article(models.Model):
    
   #null us true for now bc we have data in DB, dont want err #creates relationship with user api

    id          = models.AutoField(auto_created = True, primary_key=True, unique=True)
    title       = models.CharField(max_length = 100)
    description = models.TextField()
    #uid         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #./user_id      = models.BigIntegerField(default=False)
    #picture = models.ImaseField()
    # likess
    # comments
    # shares
    # pinned
    # date/time
    # type of event
    # location

    #token based/auth 
        #digital Ocean
        #heroku  
 

    def __str__(self):
        return self.title
