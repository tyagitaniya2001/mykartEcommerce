from django.urls import path, include
from . import views
from MyKart.urls import *

urlpatterns=[path('register',views.registration,name='register'),
   path('wallet', views.wallet, name='wallet'),
   path('MyAccount', views.MyAccount, name='MyAccount'),
   path('editprofile', views.editprofile, name='editprofile'),]