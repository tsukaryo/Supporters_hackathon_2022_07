from django.db import models

# Create your models here.

class Place:
    user_id = models.IntegerField()
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    