from django.contrib import admin
from Products.models import *
# Register your models here.
#admin.site.register(Product)


'''@admin.register(sponsor)
class sponsorAdmin(admin.ModelAdmin):
    list_display = ['id','Product.name','company','sponsormoney','keywords']
'''
admin.site.register(sponsor)

class sponsorInline(admin.StackedInline):
    model=sponsor
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        sponsorInline
    ]