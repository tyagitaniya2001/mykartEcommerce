from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
#from Customer.forms import *
from Customer.models import *
from MyKart.models import *
from Customer.views import *
from MyKart.views import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def products(request):
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    products=Product.objects.all().values()
    category = Product.objects.values_list('category').distinct()
    page = request.GET.get('page', 1)

    paginator = Paginator(products,6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products= paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    productcategory = []
    for i in range(0,len(list(category))):
        productcategory.append(list(category)[i][0])
    context = {
               'products': products,
               'category': productcategory,
    'count':c}
    return render(request,'product.html',context)



