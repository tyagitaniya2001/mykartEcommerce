from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Product(models.Model):

    class CategoryChoices(models.TextChoices):
        bodyCare = "Body Care", _("Body Care")
        electronics='Electronics',_("Electronics")
        HomeAppilances = 'Home Appliances', _("Home Appliances")
        Clothing='Clothing',_("Clothing")

    name = models.CharField(max_length=40)
    price = models.IntegerField(null=False)
    category = models.CharField(choices=CategoryChoices.choices, max_length=20)
    quantity = models.IntegerField(default=1)
    rating = models.IntegerField(null=True, blank=True)
    company = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image=models.ImageField(default='clothes.jpg',upload_to='images')
    objects = models.Manager()
    keywords = models.TextField(default=0)

class sponsor(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    sponsormoney=models.IntegerField(default=0)

