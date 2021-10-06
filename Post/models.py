from accounts.models import UserProfile
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.deletion import CASCADE
from rest_framework.authtoken.serializers import AuthTokenSerializer
 


user = settings.AUTH_USER_MODEL


class Article(models.Model):

    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
    )
    

    author = models.ForeignKey(
        UserProfile,
        default=None,
        on_delete=models.CASCADE,
       
    )

    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to="media",
        null=True,
        blank=True,
    )
    date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=False)
    longitude = models.CharField(null = True, max_length = 15)
    latitude = models.CharField(null = True, max_length = 15)
    creationDate = models.DateTimeField(default=timezone.now)
    likes        = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='like')
    event_type   = models.CharField(max_length=20, default='event', null = False)
    cover_fee    = models.IntegerField(null = True, default = 0, blank= True)
    require_mask = models.BooleanField(default= False, null = True)
    twenty_one_plus = models.BooleanField(default= False, null = True)
    
    
    # comments
    # shares
    # type of event
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    creationDate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    pos_id= models.ForeignKey(Article, on_delete=models.CASCADE)
    #for comments we will need to create a view where foreign key(post) is listing all comments.post
     
