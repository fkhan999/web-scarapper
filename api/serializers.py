from rest_framework import serializers
from .models import *

class YoutubeSerializers(serializers.ModelSerializer):
    class Meta:
        model=youtubevideos
        fields='__all__'

class GetSerializer(serializers.Serializer):
    page=serializers.IntegerField()
    page_size=serializers.IntegerField()
    def validate_page(self,data):
        if data<=0:
            raise serializers.ValidationError("Page cannot be negative or zero")
        return data

    def validate_page_size(self,data):
        if data<=0:
            raise serializers.ValidationError("Page size cannot be negative or zero")
        elif data>10:
            raise serializers.ValidationError("Page size cannot be greater than 10")

        return data