
from django.urls import path,include
from .import views

urlpatterns=[
   path("",views.login,name="login"),
   path('homepage',views.homepage,name='homepage'),
path('search',views.search,name='search'),
   path('singleproduct/cart', views.cart, name='cart'),
   path('logout', views.logout, name='logout'),
path('cate', views.cate, name='cate'),
   path('category<str:cat>', views.category, name='category'),
   path('products', views.products, name='products'),
   path('payment', views.payment, name='payment'),
   path('pay', views.pay, name='pay'),
path('singleproduct/pay', views.buynow, name='buynow'),
   path('myorders', views.myorders, name='myorders'),
   path('addbalance', views.addbalance, name='addbalance'),
   path('singleproduct/submitreview', views.submitreview, name='submitreview'),
path('mostaddedtocart', views.mostaddedtocart, name='mostaddedtocart'),
path('mostpurchaseditem', views.mostpurchaseditem, name='mostpurchaseditem'),
path('buynow/<int:id>', views.buynow, name='buynow'),
path('delete/<int:id>/<str:user>', views.delete, name='delete'),
path('addquantity/<int:id>/<str:user>/<int:price>', views.addquantity, name='addquantity'),
path('reducequantity/<int:id>/<str:user>/<int:price>', views.reducequantity, name='reducequantity'),
path('singleproduct/<int:id>', views.singleproduct, name='singleproduct')]

