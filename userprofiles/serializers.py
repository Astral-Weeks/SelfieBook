from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Selfies

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'location', 'birthday']

class SelfiesSerializer(serializers.ModelSerializer):
    class Meta():
        model = Selfies
        fields = ['user', 'selfie', 'date', 'caption']