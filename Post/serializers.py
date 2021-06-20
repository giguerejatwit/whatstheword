from django.db.models import fields
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        #create model
        model = Article
            #state fields
        fields = ['id', 'title', 'description']
  
    