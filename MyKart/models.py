from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from Products.models import Product
from datetime import date

# Create your models here.

#customers
#products
#orders
#productspurchased

def password_validator(value):
   if len(value) < 8 :
      raise ValidationError("Enter Valid Password")







class Cart(models.Model):
    customer=models.CharField(max_length=30)
    product=models.ManyToManyField(Product)
    quantity=models.IntegerField(default=0)
    totalamt=models.IntegerField(default=0)
    objects = models.Manager()

class orders(models.Model):
    customer = models.CharField(max_length=30)
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=0)
    totalamt = models.IntegerField(default=0)
    delivery=models.TextField(default="")
    objects = models.Manager()
    date=models.DateField(default=date.today())

class addedtocart(models.Model):
    productid=models.IntegerField()
    name=models.CharField(max_length=30)
    company=models.CharField(max_length=30, null=True, blank=True)


class reviews(models.Model):
    customer=models.CharField(max_length=30)
    productid=models.IntegerField()
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=30, null=True, blank=True)
    ratings=models.IntegerField()
    review=models.TextField(default="")








