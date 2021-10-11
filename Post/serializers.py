import base64
from django.http import request

from rest_framework.fields import SerializerMethodField
from accounts.models import UserProfile
from django.db.models import fields
from django.db.models.base import Model
from django.http.request import HttpHeaders
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField("_get_Avatar")
    name = SerializerMethodField("_get_Name")
    isLiked = SerializerMethodField("_isLiked")
    likeCount = SerializerMethodField("_likeCount")

    def _get_Avatar(self, article):
        user = getattr(article, "author")
        profile = UserProfile.objects.get(user=user)
        avatar_ = profile.avatar.url

        return avatar_

    def _get_Name(self, article):
        user = getattr(article, "author")
        profile = UserProfile.objects.get(user=user)
        name_ = profile.name

        return name_

    
    def _isLiked(self, article):
        user = self.context["request"].user
        isLiked = False
        hasLiked = user in article.likes.all()
        isLiked = hasLiked

        return isLiked
    
    def _likeCount(self, article):
        return article.likes.count()

    class Meta:
        # create model
        model = Article

        fields = [
            "id",
            "title",
            "description",
            "author",
            "image",
            "location",
            "date",
            "likes",
            "creationDate",
            "avatar",
            "name",
            "event_type",
            "longitude",
            "latitude",
            "isLiked",
            "likeCount"
        ]


class ArticleEditSerializer(serializers.ModelSerializer):
    class Meta:

        model = Article
        fields = [
            "title",
            "description",
            "location",
            "date",
        ]
