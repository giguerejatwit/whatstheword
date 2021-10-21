# Serializers.py creates serializers for our RegisterAPI
# we need to serializer User data, and data for when a User Registers  $$assuming we will also need a forget password serializer too
#
# #
from collections import namedtuple
from copy import error

from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone",
            "username",
            "has_agreed_tos",
        ]


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "name",
            "bio",
            "avatar",
            "instagramID",
            "snapchatID",
            "linkedinID",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField("_getEmail")
    username = serializers.SerializerMethodField("_getUsername")

    def _getEmail(self, profile):
        profile = getattr(profile, "user")

        user = User.objects.get(phone=profile.phone)
        return user.email

    def _getUsername(self, profile):
        profile = getattr(profile, "user")
        user = User.objects.get(phone=profile.phone)

        return user.username

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "email",
            "name",
            "bio",
            "username",
            "avatar",
            "instagramID",
            "snapchatID",
            "linkedinID",
            "followers",
        ]


class ViewUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField("_getEmail")
    username = serializers.SerializerMethodField("_getUsername")
    isFollowing = serializers.SerializerMethodField("_checkFollowing")

    def _checkFollowing(self, profile):

        context_user = self.context["request"].user

        pk = self.context["pk"]
        pk_user = UserProfile.objects.get(user=pk)

        c_userProfile = User.objects.get(username=context_user)

        if c_userProfile in pk_user.followers.all():

            isFollowing = True
        else:
            isFollowing = False

        return isFollowing

    def _getEmail(self, profile):
        profile = getattr(profile, "user")

        user = User.objects.get(phone=profile.phone)
        return user.email

    def _getUsername(self, profile):
        profile = getattr(profile, "user")
        user = User.objects.get(phone=profile.phone)
        return user.username

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "email",
            "name",
            "bio",
            "username",
            "avatar",
            "instagramID",
            "snapchatID",
            "linkedinID",
            "followers",
            "isFollowing",
        ]


class followSerializer(serializers.ModelSerializer):
    followers = UserProfileSerializer(
        many=True,
    )  # read_only = True)?
    following = UserProfileSerializer(
        many=True,
    )  # read_only = True)?

    class Meta:
        model = UserProfile
        fields = [
            "followers",
            "following",
        ]


#
# gives fields to http://127.0.0.1:8000/wtw/register/
#
# #
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone",
            "username",
            "email",
            "password",
            "has_agreed_tos",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["phone"],
            validated_data["password"],
            validated_data["username"],
            validated_data["has_agreed_tos"],
        )
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
