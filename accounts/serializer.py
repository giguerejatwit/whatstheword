#Serializers.py creates serializers for our RegisterAPI
# we need to serializer User data, and data for when a User Registers  $$assuming we will also need a forget password serializer too
# 
# #
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'name'
        ]

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
            'password'
        ]
        extra_kwargs =  {'password' : {"write_only": True}}
        

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone'],validated_data['password'])
        #user.save()
        return user