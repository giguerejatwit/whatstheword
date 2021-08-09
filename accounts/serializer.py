#Serializers.py creates serializers for our RegisterAPI
# we need to serializer User data, and data for when a User Registers  $$assuming we will also need a forget password serializer too
# 
# #
from collections import namedtuple
from django.db.models import fields
from rest_framework import serializers
from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'name',
            'location',
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'name',
            'bio',
            'avatar',
            'userData'
        ]
    def save(self):
        user = self.validated_data['user']
        name = self.validated_data['name']
        


#
# gives fields to http://127.0.0.1:8000/wtw/register/
# 
# 
# #
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'name'
            'password',
            'location',
        ]
        extra_kwargs =  {'password' : {"write_only": True}}
        

    def create(self, validated_data):
        #if pass
        # 
        # #
        user = User.objects.create_user(validated_data['phone'],
                                        validated_data['password'])
        #user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)