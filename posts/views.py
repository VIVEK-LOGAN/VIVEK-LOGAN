from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
import asyncio
import json
from django.http import JsonResponse
from channels.generic.websocket import WebsocketConsumer, AsyncConsumer, AsyncJsonWebsocketConsumer
from django.http import JsonResponse
import os
from django.views.decorators.csrf import ensure_csrf_cookie
import csv


def index(request):
    template = 'posts/index.html'
    productobj = ProductsModel.objects.all()
    results = feed.objects.all()
    jsondata = serializers.serialize('json', results)
    productjson = serializers.serialize('json', productobj)
    context = {
        'results': results,
        'jsondata': jsondata,
        'productjson': productjson,
        'productobj': productobj,
    }
    return render(request, template, context)


def getdata(request):
    results = feed.objects.all()
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)


def base_layout(request):
    print('YOOOOOOOOOOO!')
    template = 'posts/base.html'
    content = {
        'user': request.user
    }
    return render(request, template, context=content)


def createpost(request):
    if request.user.is_authenticated:
        error = ''
        if request.method == 'POST':
            productname = request.POST.get('productname')
            productdescription = request.POST.get('productdescription')
            producttype = request.POST.get('producttype')
            productimage = request.FILES.get('productimage')
            ProductModelOBJ = ProductsModel.objects.create(
                User=UsersModel.objects.get(User__username=request.user.username),
                ProductImage=productimage, ProductName=productname,
                ProductType=producttype,
                ProductDescription=productdescription)

            return redirect('index')
    else:
        error = 'Please Login First!'
    context = {
        'user': request.user,
        'error': error
    }
    return render(request, 'posts/createpost.html', context=context)


def LogoutView(request):
    # logout(request)
    return redirect('index')


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('wvergerb---', username, password)
        usr = User.objects.get(email=username)
        if usr is not None:
            login(request, usr)
            print('loggedin succcccesss......')
            return redirect('index')
        else:
            print('nnnnnnnoooopppppppppp ......')
            return redirect('register')
    return render(request, 'posts/login.html')


def RegisterView(request):
    if request.method == 'POST':
        UserFirstName = request.POST.get('userfirstname')
        UserLastName = request.POST.get('userlastname')
        UserEmail = request.POST.get('useremail')
        UserPhoneNumber = request.POST.get('userphone')
        UserBirthDate = request.POST.get('userbirthdate')
        UserPassword = request.POST.get('userpassword')
        UserProfileImage = request.FILES.get('userimage')
        user = User.objects.create_user(username=UserFirstName + ' ' + UserLastName, email=UserEmail,
                                        password=UserPassword)
        user.save()
        UserModelObj = UsersModel(User=User.objects.get(id=user.id), UserFirstName=UserFirstName,
                                  UserLastName=UserLastName, UserEmail=UserEmail, UserPhoneNumber=UserPhoneNumber,
                                  UserBirthDate=UserBirthDate, UserProfileImage=UserProfileImage)
        UserModelObj.save()

        usr = authenticate(username=UserFirstName + ' ' + UserLastName, password=UserPassword)
        if usr is not None:
            login(request, usr, backend='django.contrib.auth.backends.ModelBackend')
            print('loggedin succcccesss......')
            return redirect('index')
        else:
            print('nnnnnnnoooopppppppppp ......')
            return redirect('register')
    return render(request, 'posts/register.html')


def MyProductView(request):
    if request.user.is_authenticated:
        objproduct = ProductsModel.objects.filter(User__User_id=request.user.id)
        context = {
            'objproduct': objproduct
        }
    else:
        return redirect('register')
    return render(request, 'posts/myproduct.html', context=context)


def updateproduct(request, id):
    objproduct = ProductsModel.objects.get(id=id)
    if request.user.is_authenticated:
        error = ''
        if request.method == 'POST':
            productname = request.POST.get('productname')
            productdescription = request.POST.get('productdescription')
            producttype = request.POST.get('producttype')
            productimage = request.FILES.get('productimage')
            print('tttttttt---------->>>', request.user.username)
            objproduct.ProductImage = productimage
            objproduct.ProductName = productname
            objproduct.ProductType = producttype
            objproduct.ProductDescription = productdescription
            objproduct.save()
            return redirect('myproduct')
    else:
        error = 'Please Login First!'
    context = {
        'objproduct': objproduct,
        'error': error
    }
    return render(request, 'posts/updateproduct.html', context=context)


def deleteproduct(request, did):
    objproduct = ProductsModel.objects.get(id=did).delete()
    return redirect('index')


# ------------------------async-------------

# loading function
async def function_asyc():
    print('DATA STILL LOADING...')
    for i in range(5):
        await asyncio.sleep(1)
        print('second: ', i)
    print('DATA IS SUCCESSFULLY LOADED...')
    msg = 'DATA IS SUCCESSFULLY LOADED...'
    print(msg)
    return JsonResponse({'message': msg})


# second function which run before first
async def function_2(request):
    msg = 'FUNCTION WHICH RUN NO MATTER WHAT!...'
    print(msg)
    return JsonResponse({'message': msg})


def Async(request):
    if request.method == 'POST':
        async def main():
            f1 = loop.create_task(function_asyc())
            f2 = loop.create_task(function_2(request))
            await asyncio.wait([f1, f2])

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
        msg = 'SUCCESS'
        context = {
            'message': msg
        }
        return render(request, 'posts/async.html', context=context)
    return render(request, 'posts/async.html')


def Upload(request):
    if request.method == "GET":
        return render(request, 'posts/upload.html')
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        print('fiiiiiiiiiiilesssss', files)
        i = -1
        for f in files:
            print('fffffff----->>>>', f)
            UploadProductBulk.objects.create(file=f).save()
            handle_uploaded_file(f)

        return JsonResponse({'msg': '<span style="color: green;">File successfully uploaded</span>'})
    else:
        return render(request, 'posts/upload.html', )

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
