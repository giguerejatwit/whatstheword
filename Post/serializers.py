from django.db.models import fields
from django.db.models.base import Model
from django.http.request import HttpHeaders
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        #create model
        model = Article
            #state fields
        
        fields = [
            'id',
            'title',
            'description',
            'author'
            ]

