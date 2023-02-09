from django.shortcuts import render
from rest_framework.decorators import api_view
#from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes,permission_classes
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from .serializers import *
from api.models import youtubevideos
from django.core.paginator import Paginator
# Create your views here.

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def home(request,*args,**kwargs):
    page_number = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    serializer_pagination=GetSerializer(data={"page":page_number,"page_size":page_size})
    if not serializer_pagination.is_valid():
        return Response({'error':serializer_pagination.errors,"message":"Please provide correct data"},status=403)
    a1=(page_number-1)*page_size
    a2=a1+page_size
    count=youtubevideos.objects.count()
    num_of_pages=(count//page_size)+int(bool(count))
    obj=youtubevideos.objects.filter().order_by("-datetime")[a1:a2]
    serializer=YoutubeSerializers(obj,many=True)
    return Response({"total_pages":num_of_pages,"current_page":page_number,"page-size":page_size,"videos":serializer.data,"message":"Video successfully fetched"})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search(request,*args,**kwargs):
    print(request.data)
    try:
        obj=youtubevideos.objects.filter(title__icontains=request.data['title'])
        try:
            obj=obj.filter(description__icontains=request.data['description'])
        except:
            pass
    except:
        try:
            obj=youtubevideos.objects.filter(description__icontains=request.data['description'])
        except:
            obj=youtubevideos.objects.filter()
    page_number = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    serializer_pagination=GetSerializer(data={"page":page_number,"page_size":page_size})
    if not serializer_pagination.is_valid():
        return Response({'error':serializer_pagination.errors,"message":"Please provide correct data"},status=403)
    a1=(page_number-1)*page_size
    a2=a1+page_size
    count=obj.count()
    num_of_pages=(count//page_size)+int(bool(count))
    if num_of_pages==0:
        return Response({"total_pages":num_of_pages,"current_page":page_number,"page-size":page_size,"message":"There is no matching video"},404)
    obj=obj.order_by("-datetime")[a1:a2]
    serializer=YoutubeSerializers(obj,many=True)
    return Response({"total_pages":num_of_pages,"current_page":page_number,"page-size":page_size,"videos":serializer.data,"message":"Video successfully fetched"})
