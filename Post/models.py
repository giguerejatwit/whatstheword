from django.db import models

#from .serializers import ArticleSerializer

# Create your models here.
class Article(models.Model):
    id =          models.AutoField(auto_created=True, primary_key=True)
    title =       models.CharField(max_length = 100)
    description = models.TextField()
    # picture = models.ImageField()
    #token based/auth 
        #digital Ocean
        #heroku  
 

def __str__(self):
    return self.title
