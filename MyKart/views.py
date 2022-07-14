from Customer.views import *
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
#from Customer.forms import *
from Products.models import *
from Customer.models import *
from Products.views import *
from Customer.views import *
from django.db.models import Q
import requests, json
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from pgeocode import GeoDistance


# Create your views here.


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if Customer.objects.filter(username=username).exists():
            if password==Customer.objects.get(username=username).password:
                request.session['user']=username
                return redirect('homepage')
            else:
                messages.info(request,'INCORRECT PASSWORD')
                return render(request,'login.html')
        else:
            messages.info(request, 'INVALID USERNAME')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



#@login_required
def homepage(request):
    user=request.session['user']
    c=Cart.objects.filter(customer=user).count()
    products=Product.objects.all().values()[:3]

    category = Product.objects.values_list('category').distinct()
    productcategory=[]
    for i in range(0,len(list(category))):
        productcategory.append(list(category)[i][0])

    context={'user':user,
             'products':products,
             'category': productcategory,
             'count':c}
    print(context)
    return render(request,'homepage.html',context)


def cate(request):
    cat=request.POST['category']
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    products=Product.objects.filter(category=cat).values()

    context={'products':products,
                 'count':c}
    return render(request,'products.html',context)

def category(request,cat):
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    products=Product.objects.filter(category=cat).values()

    context={'products':products,
                 'count':c}
    return render(request,'products.html',context)


def singleproduct(request,id):
    user = request.session['user']
    ratings=reviews.objects.filter(productid=id)
    c = Cart.objects.filter(customer=user).count()
    id=id
    Prod=Product.objects.filter(id=id).values()
    print(Prod)
    context={'product':Prod,
             'count':c,
             'rate':ratings}
    print(context)
    return render(request,'singlepro.html',context)
global buyquan
global buyid
def cart(request):
    user = request.session['user']

    c = Cart.objects.filter(customer=user).count()
    if request.method=='POST':
        if 'addtocart' in request.POST:
            id=request.POST['addtocart']
            print(id)
            quantity=request.POST['quant']
            request.session['quan']=quantity
            if request.POST['address']:
                a= request.POST['address']
                request.session['address']=a
                c=request.POST['city']
                request.session['city']=c
                s= request.POST['state']
                request.session['state']=s
                c = request.POST['country']
                request.session['country'] = c
                pi = request.POST['pincode']
                request.session['pincode'] = pi
            else:
                a=Customer.objects.get(username=user).address
                request.session['address'] = a
                c=Customer.objects.get(username=user).city
                request.session['city'] = c
                s=Customer.objects.get(username=user).state
                request.session['state'] = s
                c=Customer.objects.get(username=user).country
                request.session['country'] = c
                pi=Customer.objects.get(username=user).pincode
                request.session['pincode'] = pi
            quan= Product.objects.get(id=id).quantity
            if int(quantity)>int(quan):
                messages.info(request,'OUT OF STOCK!!!')
                return redirect('singleproduct',id)
            if int(quantity)<=0:
                messages.info(request, 'Select Valid Quantity')
                return redirect('singleproduct', id)

            p=Product.objects.filter(id=id).values()
            print(p)
            totalamt=1
            for i in p:
                print(i)
                totalamt=totalamt*int(quantity)*i['price']
            user=request.session['user']



            cart=Cart(customer=user,quantity=quantity,totalamt=totalamt)
            cart.save()
            cart.product.add(id)

            cart.save()
            ca=cart.product.all()
            print(ca)
            for i in ca:
                print(i.name)
            new=int(quan)-int(quantity)
            Product.objects.filter(id=id).update(quantity=new)
            pname=Product.objects.get(id=id).name
            pcompany=Product.objects.get(id=id).company
            addedtocart.objects.create(productid=id,name=pname,company=pcompany)

            messages.info(request,'Product Added To Cart')
            return redirect('singleproduct',id)
        elif 'buynow' in request.POST:

            user = request.session['user']
            if request.POST['address']:

                a = request.POST['address']
                request.session['address'] = a
                c = request.POST['city']
                request.session['city'] = c
                s = request.POST['state']
                request.session['state'] = s
                c = request.POST['country']
                request.session['country'] = c
                pi = request.POST['pincode']
                request.session['pincode'] = pi
            else:
                a = Customer.objects.get(username=user).address
                request.session['address'] = a
                c = Customer.objects.get(username=user).city
                request.session['city'] = c
                s = Customer.objects.get(username=user).state
                request.session['state'] = s
                c = Customer.objects.get(username=user).country
                request.session['country'] = c
                pi = Customer.objects.get(username=user).pincode
                request.session['pincode'] = pi
            c = Cart.objects.filter(customer=user).count()
            bal = Customer.objects.get(username=user).walletbalance
            global buyid
            id=request.POST['buynow']
            buyid=id
            quantity = request.POST['quant']
            global buyquan
            buyquan=quantity
            print(buyquan)
            if int(buyquan) < 1:
                messages.info(request, 'enter valid quantity')
                return redirect('singleproduct', id)
            p = Product.objects.filter(id=id).values()
            print(p)
            geolocator = Nominatim(user_agent="Mykart")
            dist=GeoDistance('in')
            #print(pincode)
            try:
                pincode=request.session['pincode']
                distance=dist.query_postal_code(pincode,'201017')

                print("distance is " + str(distance))
            #print("pincode"+str(pincode))


                if distance < 100:
                    deltime = 1
                    delcharge=20
                else:
                    deltime = distance / 100
                    deltime = int(deltime)+1
                    delcharge = 0.5 * int(distance)
            except:
                messages.info(request, 'Invalid Address!!!')
                return redirect('singleproduct', id)
            totalamt = 1
            total=0
            for i in p:
                print(i)
                totalamt = totalamt * int(buyquan) * i['price']
                total=total+totalamt+int(delcharge)

            return render(request,'payment.html', {'price': int(totalamt), 'count': c,
                                                   'bal': bal,'total':total,'delcharge':int(delcharge),'deltime':deltime})


    else:
        products=Cart.objects.filter(customer=user).order_by('-id')
        print(products)
        ids=[]
        for p in products:
            pro=p.id
            ids.append(pro)
        print(ids)
        request.session['products']=ids
        print('saves')
        context={'products':products,
                 'count':c}
        return render(request,"cart.html",context)

def buynow(request):
    use = request.session['user']
    geolocator = Nominatim(user_agent="Mykart")
    dist = GeoDistance('in')
    # print(pincode)
    try:
        pincode = request.session['pincode']
        distance = dist.query_postal_code(pincode, '201017')

        print("distance is " + str(distance))
        # print("pincode"+str(pincode))

        if distance < 100:
            deltime = 1
            delcharge = 20
        else:
            deltime = distance / 100
            deltime = int(deltime) + 1
            delcharge = 0.5 * int(distance)
    except:
        messages.info(request, 'Invalid Address!!!')
        return redirect('singleproduct', id)

    c = Cart.objects.filter(customer=use).count()
    bal = Customer.objects.get(username=use).walletbalance
    quantity=buyquan
    if request.method == 'POST':
        pas = request.POST['password']
        amt = request.POST['pay']
        passw = Customer.objects.get(username=use).password
        if pas != passw:
            messages.info(request, 'Wrong password')
            return render(request, 'payment.html', {'price': int(amt)-int(delcharge), 'count': c,
                                                   'bal': bal,'total':amt,'delcharge':int(delcharge),'deltime':deltime})
        user = Customer.objects.get(username=use).walletbalance
        if int(amt) > int(user):
            messages.info(request, 'Insufficient balance in wallet')
            return render(request, 'payment.html', {'price': int(amt)-int(delcharge), 'count': c,
                                                   'bal': bal,'total':amt,'delcharge':int(delcharge),'deltime':deltime})
        else:
            user = Customer.objects.get(username=use).walletbalance
            new = int(user) - int(amt)
            print(new)
            Customer.objects.filter(username=use).update(walletbalance=new)
            add=request.session['address']
            ci=request.session['city']
            st=request.session['state']
            co=request.session['country']
            pi=request.session['pincode']

            delivery=add+','+ci+','+st+','+co+'-'+str(pi)
            order = orders(customer=use, quantity=quantity, totalamt=amt,date=date.today(),delivery=delivery)
            order.save()

            order.product.add(buyid)
            order.save()
        return redirect('myorders')




def payment(request):
    user=request.session['user']
    geolocator = Nominatim(user_agent="Mykart")

    dist = GeoDistance('in')
    print(pincode)
    try:
        distance = dist.query_postal_code(pincode, '201017')

        print("distance is " + str(distance))
        # print("pincode"+str(pincode))


        if distance < 100:
            deltime = 1
            delcharge=20
        else:
            deltime = distance / 100
            deltime = int(deltime) + 1
            delcharge = 0.5 * int(distance)
    except:
        messages.info(request, 'Selected Address is Invalid , '
                               'We do not deliver to this address!!!')
        return redirect("cart")
    c = Cart.objects.filter(customer=user).count()
    bal = Customer.objects.get(username=user).walletbalance
    amts=Cart.objects.filter(customer=user).values()
    print(amts)
    list=[]
    for i in amts:
        print(i)
        list.append(i['totalamt'])
    print(list)

    total=0
    for a in list:
        total=total+a
    return render(request,'payment.html',{'total':total+int(delcharge),'count':c,'bal':bal,
                                          'delcharge':int(delcharge),'deltime':deltime,'price':total})

def pay(request):
    use=request.session['user']
    if request.method=='POST':
        pas=request.POST['password']
        amt=request.POST['pay']
        passw = Customer.objects.get(username=use).password
        if pas != passw:
            messages.info(request,'Wrong password')
            return redirect('payment')
        user=Customer.objects.get(username=use).walletbalance
        if int(amt)>int(user):
            messages.info(request,'Insufficient balance in wallet')
            return redirect('payment')
        else:
            user = Customer.objects.get(username=use).walletbalance
            new=int(user)-int(amt)
            print(new)
            Customer.objects.filter(username=use).update(walletbalance=new)
            print("updated")
            p=request.session['products']
            print("price"+str(p))
            for i in range(0,len(p)):
                ord=Cart.objects.get(id=p[i])
                print(ord)
                add = request.session['address']
                ci = request.session['city']
                st = request.session['state']
                co = request.session['country']
                pi = request.session['pincode']

                delivery = add + ',' + ci + ',' + st + ',' + co + '-' + str(pi)
                order=orders(customer=ord.customer,quantity=ord.quantity,totalamt=ord.totalamt,
                             date=date.today(),delivery=delivery)
                order.save()
                for i in ord.product.all():
                    order.product.add(i.id)
                    order.save()
                ord.delete()
            return redirect('myorders')



def myorders(request):
    user = request.session['user']
    c = Cart.objects.filter(customer=user).count()
    order = orders.objects.filter(customer=user).order_by('-id')
    print('saves')
    context = {'orders': order,
               'count':c}
    return render(request, "myorders.html", context)

def delete(request,id,user):

    c=Cart.objects.filter(customer=user,id=id)
    print(c)
    c.delete()
    products = Cart.objects.filter(customer=user)
    print(products)
    ids = []
    for p in products:
        pro = p.id
        ids.append(pro)
    print(ids)
    request.session['products'] = ids
    print('saves')
    co = Cart.objects.filter(customer=user).count()
    context = {'products': products,
               'count': co}
    return render(request, "cart.html", context)

def addquantity(request,id,user,price):
    product=Cart.objects.filter(customer=user,id=id).values()
    print(product)
    for i in product:
        print(i)
        quan=i['quantity']+1
        amt=i['totalamt']+price
        print(amt)
        products = Cart.objects.filter(customer=user,id=id).update(quantity=quan,totalamt=amt)
    co = Cart.objects.filter(customer=user).count()
    prod = Cart.objects.filter(customer=user).order_by('-id')
    print(prod)
    context = {'products': prod,
               'count': co}
    return render(request, "cart.html", context)

def reducequantity(request,id,user,price):
    product=Cart.objects.filter(customer=user,id=id).values()
    print(product)
    for i in product:
        print(i)
        quan=i['quantity']-1
        print(quan)
        amt=i['totalamt']-price
        print(amt)
        if quan<1 or amt<1:
            products = Cart.objects.filter(customer=user, id=id).delete()
        else:

            products = Cart.objects.filter(customer=user,id=id).update(quantity=quan,totalamt=amt)
    co = Cart.objects.filter(customer=user).count()
    prod = Cart.objects.filter(customer=user).order_by('-id')
    print(prod)
    context = {'products': prod,
               'count': co}
    return render(request, "cart.html", context)


def search(request):
    if request.method=='POST':
        key=request.POST['keyword'].lower()
        if Product.objects.filter(Q(category__iexact=key)|Q(name__iexact=key)|Q(company__iexact=key)).exists():
            prod=Product.objects.filter(Q(category__iexact=key)|Q(name__iexact=key)|Q(company__iexact=key))
            print(list(prod))
            products=[]
            ids=Product.objects.filter(Q(category__iexact=key)|Q(name__iexact=key)|Q(company__iexact=key)).values_list('id')
            idlist=[]
            for i in ids:
                idlist.append(i[0])
            print(idlist)
            p=sponsor.objects.all().order_by('-sponsormoney')
            splist=[]
            for i in p:
                splist.append(i.product.id)
            print(splist)
            sponsors=[]
            for i in idlist:
                if i in splist:
                    sponsors.append(i)
            print(sponsors)
            pro=[]
            for i in sponsors:
                p=Product.objects.get(id=i)
                pro.append(p)
            for i in list(prod):
                    if i not in pro:
                        products.append(i)
                    else:
                        pass
            print(pro)
            print(products)
        else:
            prod=Product.objects.filter(Q(category__icontains=key)|
                                                       Q(description__icontains=key)|
                                                       Q(name__icontains=key)|
                                                       Q(company__icontains=key)|
                                        Q(keywords__icontains=key))
            print(list(prod))
            products = []
            if prod:
                ids = Product.objects.filter(Q(category__icontains=key)|
                                                       Q(description__icontains=key)|
                                                       Q(name__icontains=key)|
                                                       Q(company__icontains=key)|
                                         Q(keywords__icontains=key)).values_list('id')
                idlist = []
                for i in ids:
                    idlist.append(i[0])
                print(idlist)
                p = sponsor.objects.all().order_by('-sponsormoney')
                splist = []
                for i in p:
                    splist.append(i.product.id)
                print(splist)
                sponsors = []
                for i in idlist:
                    if i in splist:
                        sponsors.append(i)
                print(sponsors)
                pro = []
                for i in sponsors:
                    p = Product.objects.get(id=i)
                    pro.append(p)
                for i in list(prod):
                    if i not in pro:
                        products.append(i)
                    else:
                        pass
                print(pro)
                print(products)

                context = {'products': products,'pro':pro}
                return render(request, 'products.html', context)
            else:
                messages.info(request,'This Product is not available')
                return render(request, 'products.html')


def mostaddedtocart(request):
    products=addedtocart.objects.all()
    print(products)
    max=0
    maxid=0
    for i in products:
        c=0
        id=i.productid
        c=addedtocart.objects.filter(productid=id).count()
        if c>max:
            max=c
            maxid=id
    print(max)
    print(maxid)
    mostaddedp=Product.objects.filter(id=maxid)
    for i in mostaddedp:
        print(i.name)
        print(i.company)


def mostpurchaseditem(request):
    products = orders.objects.all()
    print(products)
    max = 0
    maxid = 0
    for i in products:
        c = 0
        ide = i.product
        print(ide)
        for i in ide:
            id=i.id

            c = orders.objects.filter(product=id).count()
            if c > max:
                max = c
                maxid = id
    print(max)
    print(maxid)
    mostaddedp = Product.objects.filter(id=maxid)
    for i in mostaddedp:
        print(i.name)
        print(i.company)


def submitreview(request):
    c=0
    user=request.session['user']
    if request.method=='POST':
        ide=request.POST['iproduct']
        if 'review' in request.POST:
            review = request.POST['review']
        pro=Product.objects.get(id=ide)
        name=pro.name
        company=pro.company
        if 'star1' in request.POST:

            c = request.POST['star1']
        if 'star2' in request.POST:
            c= request.POST['star2']
        if 'star3' in request.POST:
            c = request.POST['star3']
        if 'star4' in request.POST:
            c=request.POST['star4']
        if 'star5' in request.POST:
            c= request.POST['star5']

        print("ratings : "+ str(c))
        reviews.objects.create(customer=user,productid=ide,name=name,company=company,ratings=c,review=review)
        return redirect('singleproduct',ide)






def logout(request):
    del request.session['user']
    return redirect('login')









