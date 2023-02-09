from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self, data):
        user=User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()
        return user