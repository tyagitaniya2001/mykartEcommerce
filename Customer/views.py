from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
#from Customer.forms import *
from Products.models import *
from MyKart.models import *
from Products.views import *
from MyKart.views import *
from datetime import date
from django.contrib.auth.hashers import make_password


# Create your views here.
def registration(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        print(request.POST)
        age = request.POST['age']
        address= request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        password=request.POST['password']
        print (make_password (password))
        confirm=request.POST['confirm']
        data={'firstname':firstname,
              'lastname':lastname,
              'username':username,
              'age':age,
              'phone':phone,
              'email':email,
              'address':address,
              'city':city,
              'state':state,
              'country':country,
              'pincode':pincode}
        if Customer.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME ALREADY TAKEN')
            return render(request, 'register.html',{'data':data})
        if Customer.objects.filter(email=email).exists():
            messages.info(request, 'EMAIL USED FOR ANOTHER ACCOUNT')
            return render(request, 'register.html',{'data':data})
        if Customer.objects.filter(phone=phone).exists():
            messages.info(request, 'MOBILE NUMBER USED FOR ANOTHER ACCOUNT')
            return render(request, 'register.html',{'data':data})
        if len(password)<8:
            messages.info(request, 'Password must be greater than 8 digits and contain number,alphabets')
            return render(request, 'register', {'data': data})
        if password==confirm:
            Customer.objects.create(username=username,firstname=firstname,lastname=lastname,age=age,phone=phone,email=email,
                                    address=address,city=city,state=state,country=country,pincode=pincode,password=password,walletbalance=0)
            messages.info(request, 'REGISTERED SUCCESSFULLY')
            return redirect('login')
        else:
            messages.info(request, 'PASSWORD NOT MATCHING!')
            return render(request, 'register.html', {'data': data})
    else:
        #form=RegistrationForm()
        return render(request, 'register.html')

def wallet(request):
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    bal = Customer.objects.get(username=user).walletbalance

    return render(request, 'wallet.html', {'bal': bal,'count':c})

def addbalance(request):
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()

    if request.method=='POST':
            user = request.session['user']
            bal = Customer.objects.get(username=user).walletbalance
            addbal = request.POST['money']
            name = request.POST['name']
            credit = request.POST['creditnum']
            cv = request.POST['cvv']
            expdate = request.POST['date']
            if credit.isnumeric() == False or len(credit) < 12:
                messages.info(request, 'Invalid credit card number')
                return render(request, 'addbalance.html')
            elif len(cv) != 3:
                messages.info(request, 'CVV Number is not valid')
                return render(request, 'addbalance.html')
            elif name.isnumeric()==True or name.isalnum()==True  :
                messages.info(request, 'Invalid Name')
                return render(request, 'addbalance.html')
            elif str(expdate) < str(date.today()):
                messages.info(request, 'Card already expired')
                return render(request, 'addbalance.html')
            newbal = int(bal) + int(addbal)
            print(newbal)
            Customer.objects.filter(username=user).update(walletbalance=newbal)
            messages.info(request, 'Balance Added!')
            return render(request, 'wallet.html', {'bal': newbal,'count':c})
    else:
        return render(request,'addbalance.html',{'count':c})



def MyAccount(request):
    user=request.session['user']

    c = Cart.objects.filter(customer=user).count()
    me=Customer.objects.filter(username=user).values()
    return render(request,'mydetails.html',{'data':me,'count':c})


def editprofile(request):
    user = request.session['user']
    #user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    u = Customer.objects.get(username=user)
    data = {'username': u.username,
            'firstname': u.firstname,
            'lastname': u.lastname,
            'age': u.age,
            'address':u.address,
            'count':c,
            'city':u.city,
            'country':u.country,
            'state':u.state,
            'pincode':u.pincode,

            }
    if request.method=='POST':
        #username=request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        address = request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        pincode=request.POST['pincode']
        if request.POST['password']:

            password=request.POST['password']
        else:
            password=u.password
        confirm=request.POST['confirm']
        context = {
                'firstname': firstname,
                'lastname': lastname,
                'age': age,
                'address': address,
            'city': city,
            'country': country,
            'state': state,
            'pincode': pincode,
                   'count':c
                   }


        if len(password)<8:
            messages.info(request, 'Password must be greater than 8 digits and contain number,alphabets')
            return render(request, 'editprofile.html', {'data': context})

        if confirm==u.password:
            Customer.objects.filter(username=user).update(firstname=firstname,lastname=lastname,
                                                      age=age,address=address,city=city,state=state,country=country,
                                                          pincode=pincode,password=password)
            u = Customer.objects.get(username=user)
            data = {'username': u.username,
                'firstname': u.firstname,
                'lastname': u.lastname,
                'age': u.age,
                'address': u.address,
                'phone':u.phone,
                    'count':c,
                    'city': u.city,
                    'country': u.country,
                    'state': u.state,
                    'pincode': u.pincode,
                }
            messages.info(request, 'Updated Successfully!')
            return render(request, 'editprofile.html', {'data': data})
        else:
            messages.info(request, 'Wrong password!')
            return render(request, 'editprofile.html', {'data': context})

    else:
        return render(request, 'editprofile.html', {'data': data})
