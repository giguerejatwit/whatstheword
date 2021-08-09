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
        user,
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
    creationDate = models.DateTimeField(default=timezone.now)
    # likes
    # comments
    # shares
    # type of event
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    creationDate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    
