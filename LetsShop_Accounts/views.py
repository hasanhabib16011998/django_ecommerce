from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import uuid
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

#User Login/Logout functionality
#--------------------------------------------------------------------

def Login(request):
    if request.method=='POST':
        User_name=request.POST.get('username')
        Password=request.POST.get('password')
        if len(Password)==0:
            messages.warning(request,"No password found!")
            return redirect('login')
        user=authenticate(username=User_name,password=Password)
        if user:
            prof=Profile.objects.get(user=user)
            if prof.is_verified==True:
                login(request,user)
                return redirect('User_dash')
            else:
                return redirect('Error')
        else:
            messages.error(request,"Password or username is not found!")
    return render(request,'Accounts/login.html')

def Logout(request):
    logout(request)
    messages.warning(request,"You are logged out")
    return redirect('Login')
#--------------------------------------------------------------
#user email verified registration:
#--------------------------------------------------------------
def Registration(request):
    if request.method=='POST':
        User_name=request.POST.get('username')
        First_name=request.POST.get('firstname')
        Last_name=request.POST.get('lastname')
        Email=request.POST.get('email')
        Password=request.POST.get('pass')
        Retyped_password=request.POST.get('pass1')

        if User_name is not None:
            for i in User_name:
                if i in ['.','@','/','%','*','$']:
                    messages.warning(request,"Your username contains special characters. Please remove them.")
                    return redirect('Registration')

            if User.objects.filter(username='User_name').exists():
                messages.warning(request,"Your username is already taken. Try New!")
            elif User.objects.filter(email='Email').exists():
                messages.warning(request,"Your Email is already taken. Try another!")
            else:
                if Retyped_password==Password:
                    user=User.objects.create_user(username=User_name,first_name=First_name,last_name=Last_name,email=Email,password=Password)
                    user.set_password(Password)
                    auth_token=str(uuid.uuid4())
                    pro_obj=Profile.objects.create(user=user,auth_token=auth_token)
                    pro_obj.save()
                    send_mail_registration(Email,auth_token)
                    return redirect('Success')
                else:
                    messages.warning(request,"Your password did not match. Try again.")

        print(First_name,Last_name,Password)


    return render(request,'Accounts/registration.html')

def Success(request):
    return render(request,'Accounts/success.html')

def Token(request):
    return render(request,'Accounts/token_send.html')

def Error(request):
    return render(request,'Accounts/error.html')

def send_mail_registration(Email,auth_token):
    subject='Your Account Authentication Link'
    message=f'Hi,Here is your verification link for your account: http://127.0.0.1:8000/accounts/verify/{auth_token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[Email]
    send_mail(subject,message,email_from,recipient_list)

def verify(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified=True
    profile_obj.save() 
    messages.success(request,"Wow,It's Done.")
    return redirect('Login')
#----------------------------------------------------------------------
#Password reset functionality
#----------------------------------------------------------------------
def Reset_pass(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if email:
            user_prof=User.objects.filter(email=email)
            if user_prof:
                res_prof=Profile.objects.get(user=user_prof)
                auth_token=res_prof.auth_token
                print(auth_token)
                send_mail_reset(email,auth_token)
                return redirect('Success')
            else:
                messages.error(request,"Mail Address not found.")
                return redirect('Reset_pass')
    return render(request,'Accounts/reset_pass.html')


def send_mail_reset(Email,auth_token):
    subject='Your Account Reset Password Link'
    message=f'Hi,Here is your verification link for your password reset: http://127.0.0.1:8000/accounts/Reset_user_pass/{auth_token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[Email]
    send_mail(subject,message,email_from,recipient_list)

def Reset_user_pass(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if request.method=='POST':
            Password=request.POST.get('password')
            Password1=request.POST.get('password1')
            if Password==Password1:
                user=profile_obj.user
                user.set_password(Password)
                user.save()
                messages.success(request,"Your Password has been changed successfully.")
                return redirect('Login')
            else:
                messages.warning(request,"Your password and retyped password does not match.Try again!")
                
    return render(request,'Accounts/new_pass.html')
#----------------------------------------------------------------------



#----------------------------------------------------------------------
#User Dashboard:
#----------------------------------------------------------------------

def User_dash(request):
    user=request.user
    print(user)
    address=Address.objects.filter(user=user)
    print(address)
    return render(request,'Accounts/User_dash.html',locals())
