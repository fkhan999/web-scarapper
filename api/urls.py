from django.contrib import admin
from django.urls import path,include
from api import views
#from rest_framework.authtoken import views

urlpatterns = [
    path('get/', views.home),
    path("search/",views.search),
]

