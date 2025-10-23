from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    address  = models.CharField(max_length=150)
    gender  = models.CharField(max_length=10)
    password = models.CharField(max_length=255,default="default")






    
