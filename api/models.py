from django.db import models

# Create your models here.

class youtubevideos(models.Model):
    id=models.CharField(max_length=100,primary_key=True)
    title=models.TextField()
    description=models.TextField(default="No description")
    thumbnail=models.URLField()
    datetime=models.DateTimeField()
