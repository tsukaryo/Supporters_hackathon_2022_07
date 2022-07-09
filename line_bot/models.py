from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200,blank=True,null=True)

    
class Status(models.Model):
    place_id = models.IntegerField()
    status = models.IntegerField()