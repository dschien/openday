from django.db import models

# Create your models here.
class Contact(models.Model):
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)
