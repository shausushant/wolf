from ctypes.wintypes import MSG
from distutils.log import error
# from nis import cat
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from importlib_metadata import email
from matplotlib.pyplot import flag
from numpy import save
from .models import Category, register, product,order
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.

def index(request):
    if request.method =="POST":
        product_id = request.POST.get('cartid')
        remove = request.POST.get('minus')
        cart_id = request.session.get('cart')
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <=1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity -1
                else:
                    cart_id[product_id] = quantity +1
            else:
                cart_id[product_id] = 1
        else:
            cart_id ={}
            cart_id[product_id] = 1
        request.session['cart'] = cart_id
        print(request.session['cart'])

    path = product.objects.all()
    # print(path)
    # return render(request,'home.html',{'path': path})
    # path = product.obeject.all()
    cat = Category.objects.all()
    cat_id =request.GET.get('category')
    if cat_id:
        path = product.objects.filter(category_id=cat_id)
    else:
        path = product.objects.all()
    return render(request, 'home.html',{'path': path,'cate':cat})

def home(request):
    return render((request),"home.html")

def contact(request):
    return render(request,'contact.html')



def save_info(request):
    if request.method =='POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        save_info = register(firstname=fname, lastname=lname,
                            mobile=mobile, password=password,gender=gender, email=email)
        save_info.save()
        return redirect('home')
def register_info(request):
    fname = request.POST.get('firstname')
    lname = request.POST.get('lastname')
    mobile = request.POST.get('mobile')
    gender = request.POST.get('gender')
    email = request.POST.get('email')
    password = request.POST.get('password')
    # print('success')

    store_data = register(firstname=fname, lastname=lname, mobile=mobile, gender=gender, email=email,password=make_password(password))
    store_data.save()

    return HttpResponse("success")

def login_info(request):
    error_msg = None
    if request.method == "POST":
        email = request.POST.get('email')
        password =request.POST.get('password')
        print(email)
        print(password)
        try:
            fetch_email = register.objects.get(email=email)
            print(fetch_email)
            if (fetch_email.email==email):
                print(fetch_email)
                request.session['email'] = fetch_email.email
                request.session['id'] = fetch_email.id

                request.session['firstname'] = fetch_email.firstname
                
                flag=check_password(password,fetch_email.password)
                if flag:
                    print(True)
                    request.session['email']=fetch_email.email
                    request.session['customer_id']=fetch_email.id
                    request.session['firstname']=fetch_email.firstname
                    return redirect('home')
                else:
                    error_msg = "invalid password"
                    return render (request,'home.html' , {'error_msg' : error_msg })

        except:
            error_msg = "Please Enter vaild Email"
            return render (request,'home.html' , {'error_msg' : error_msg })

        return HttpResponse(fetch_email.email, fetch_email.password)

def logout(request):
    request.session.clear()
    return redirect('home')

def cart (request):
    ids=list(request.session.get('cart').keys())
    print(ids)
    cart_pro = product.objects.filter(id__in = ids)
    # print(cart_pro)
    return render (request,'cart.html',{'cart_pro':cart_pro})


def checkout (request):
    if request.method == "POST":
        address=request.POST.get("address")
        mobile=request.POST.get("mobile")
        customer_id = request.session.get('customer_id')
        cart= request.session.get('cart')
        products = product.objects.filter(id__in=list(cart.keys()))

        for pro in products:
            save_order_dtls = order(
                customer=register(id=customer_id),
                product=pro,
                price=pro.price,
                quantity=cart.get(str(pro.id)),
                address=address,
                phone=mobile
                )
            save_order_dtls.save()
            request.session['cart']={}
    return redirect('cart')
    # return render(request,'order.html')


def order_dtl(request):
    customer = request.session.get('customer_id')
    ord_Dtls =order.objects.filter(customer=customer).order_by('-date')
    tp = 0
    for i in ord_Dtls:
        tp = tp+(i.price *i.quantity)


    return render(request,'order.html',{'ord_dtls':ord_Dtls,'tp':tp})

