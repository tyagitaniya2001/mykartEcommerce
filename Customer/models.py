from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=30,unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    age=models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=40,default='')
    city=models.CharField(max_length=40,default='')
    state=models.CharField(max_length=40,default='')
    country=models.CharField(max_length=40,default='')
    pincode= models.IntegerField(default=0)
    password = models.CharField(max_length=20)
    walletbalance=models.IntegerField()
    objects=models.Manager()