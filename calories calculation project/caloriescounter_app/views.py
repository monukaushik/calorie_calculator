from django.shortcuts import render,redirect
from .models import *
import requests
import random
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import datetime
import math
from django.db.models import Sum



def index(request):
    if request.method=='POST':
      username=request.POST.get('username')
      password=request.POST.get('password')
      user=authenticate(request,username=username,password=password)
      if user is not None:
         auth.login(request,user)
         if user.is_superuser:
            return redirect('/admin_panel/')
         else:
            return redirect ('/calorie_count/')
      else:
            messages.error(request,'user is none')
    return render(request,'index.html')

@login_required
def calorie_summary(request):
    if request.method != 'POST':
        return render (request,'calorie_summary.html')
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = request.POST.get('food')
    cur_date=request.POST.get('date')
    username=request.POST.get('name')
    total_cal=request.POST.get('calorie')
    consume_cal=0
    response = requests.get(api_url + query, headers={'X-Api-Key': 'z02bo2D/cA8eBgC6UbGcfw==msLLQmxmCaoYH9Xx'})
    try:
        result=response.json()['items'][0]
        food_item=result['name']
        calories=int(result['calories'])
        protein=int(result['protein_g'])
        fat=int(result['fat_total_g'])
        carbs=int(result['carbohydrates_total_g'])
        suger=int(result['sugar_g'])

        save_data=food_item_gredient.objects.create(
                        username=username,
                        date=cur_date,
                        total_cal=total_cal,
                        consume_calorie=consume_cal,
                        food_item=food_item,
                        calories=calories,
                        protein=protein,
                        fat=fat,
                        carbs=carbs,
                        suger=suger,
                      )
        save_data.save()
        user=request.user.username
        cur_date=datetime.datetime.now()
        data=food_item_gredient.objects.filter(date=cur_date,username=user)
        total_consume=food_item_gredient.objects.filter(date=cur_date,username=user).aggregate(Sum('calories'))
        value=total_consume.get('calories__sum')   
        balance=int(total_cal)-value
    except:
        balance=None
    return render (request,'calorie_summary.html',{'total_cal':total_cal,'data':data,'total_consume':value,'balance':balance})


@login_required
def calorie_count(request):
    if request.method != 'POST':
        return render(request,'calorie_count.html')
    weight=request.POST.get('weight')
    height=request.POST.get('height')
    age=request.POST.get('age')
    gender=request.POST.get('gender')

    if gender=='Male':
        result = 66.47 + (13.75 * int(weight)) + (5.003 * int(height)) - (6.755 * int(age))
    else:
        result= 655.1 + (9.563 * int(weight)) + (1.850 * int(height)) - (4.676 * int(age))
    calorie=math.ceil(result)
    return render(request,'calorie_count.html',{'total_calorie':calorie})

def signup(request):
     if request.method == 'POST':
        username=request.POST.get('username')
        useremail=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if password == cpassword:
            user=User.objects.create_user(username=username,email=useremail,password=password)
            user.save()
            return redirect('/')  
        else:
            messages.error(request,'password not match!!')
     return render(request,'signup.html')
 
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

def forgot_username(request):
    if request.method=='POST':
        username=request.POST.get('username')
        username1=User.objects.get(username=username)
        if username1 is not None:
            otp=random.randint(1000,9999)
            request.session['otp']= otp
            request.session['username']= username

            subject = 'OTP for reset password'
            message = 'This otp use for forgot password %d' % otp
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [username1.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return redirect('/forgot_otp/')
        else:
            messages.error(request,'username is none')
    return render(request,'forgot_username.html')

def forgot_otp(request):
    if request.method=='POST':
        otp= int(request.POST.get('otp'))
        session_otp=request.session.get('otp',None)
        if otp==session_otp:
            return redirect('/forgot_password/')
        else:
            return redirect('/forgot_otp/')
    return render(request,'forgot_otp.html')

def forgot_password(request):
    if request.method=='POST':
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            username=User.objects.get(username=request.session.get('username'))
            if username is not None:
                username.set_password(password)
                username.save()
                return redirect('/')
            else:
                messages.error(request,'username is none')
                return redirect('forgot_password')
        else:
            messages.error(request,'password does not match !!')       
    return render(request,'forgot_password.html')


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')





