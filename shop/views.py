from django.shortcuts import render
from django.contrib.messages import success, error
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.core.mail import send_mail
from shop.models import *
import random
import string
from Vendor_Management_System import settings

# Create your views here.

def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' it  means a lot to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )

def register(request):
    if(request.method=='POST'):
        lname=request.POST.get('uname')
        lpward=request.POST.get('psw')
        user=auth.authenticate(username=lname,password=lpward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/showpage')
            else:
                return HttpResponseRedirect('/view')
        else:
            error(request,"Invalid User")
    return render(request,'userLogin.html')

def signUp(request):
    if(request.method=='POST'):
        unam=request.POST.get('uname')
        try:
            match = User.objects.get(username=str(unam))
            if (match):
                error(request, "Username Already Exist")

        except:
            fnam = request.POST.get('first_name')
            lnam = request.POST.get('last_name')
            mail = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if (pward == cpward):
                User.objects.create_user(username=str(unam),
                                         first_name=str(fnam),
                                         last_name=str(lnam),
                                         email=mail,
                                         password=pward
                                         )
                success(request, "Account is created")
                try:
                    email_send(request, mail, unam)
                except:
                    error(request, " ")
                return HttpResponseRedirect('/')
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request, "Signup.html")

def deleteShop(request,shop_id):
    sd = Shop.objects.get(id=shop_id)
    sd.delete()
    sl = Shop.objects.filter(vendor=request.user)
    return render(request, "vendor.html", {"s": sl})

@login_required(login_url='/')
def addShop(request):
    if request.method == 'POST':
        res = ''.join(random.choices(string.digits, k=7))
        sro = Shop()
        sro.id = res
        sro.sid = request.POST.get('shopid')
        cn = request.POST.get('cat')
        ct = Category.objects.get(cname=cn)
        sro.cat = ct
        sro.name = request.POST.get('shopname')
        sro.description = request.POST.get('description')
        img1 = request.FILES.get('uimage1')
        img2 = request.FILES.get('uimage2')
        if img1:
            sro.img1 = img1
        if img2:
            sro.img2 = img2
        sro.latitude = request.POST.get('latitude')
        sro.longitude = request.POST.get('longitude')
        sro.address = request.POST.get('address')
        sro.vendor = request.user
        sro.save()

        success(request, 'Saved successfully')

    cat = Category.objects.all()
    return render(request,"AddShop.html",{"Cat":cat})


@login_required(login_url='/')
def editShop(request,shop_id):
    s = Shop.objects.get(id=shop_id)
    cat = Category.objects.all()
    if request.method == 'POST':
        cn = request.POST.get('cat')
        ct = Category.objects.get(cname=cn)
        s.cat = ct

        s.name = request.POST.get('name')
        s.description = request.POST.get('description')
        img1 = request.FILES.get('uimage1')
        img2 = request.FILES.get('uimage2')
        if img1:
            s.img1 = img1
        if img2:
            s.img2 = img2
        s.latitude = request.POST.get('latitude')
        s.longitude = request.POST.get('longitude')
        s.address = request.POST.get('address')
        s.save()
        success(request, 'Saved successfully')

    return render(request,"EditShop.html",{"s":s,"cat":cat})

@login_required(login_url='/')
def showPage(request):
    shops = Shop.objects.filter(vendor=request.user)

    return render(request,"vendorpage.html",{"s":shops})

@login_required(login_url='/')
def shopView(request):
    shops = Shop.objects.all()
    cat = Category.objects.all()

    return render(request,"customerpage.html",{"Data":shops,"cat":cat})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')




