from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib.auth import logout
from django.contrib import auth
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        if username == "" or password=="":
            return redirect("/login")
        else:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(req,user)
                if req.user.is_superuser:
                    return redirect('/admin_home')
                return redirect('/')
            else:
                messages.error(req, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!")
                return redirect('/login')
    return render(req, 'login.html')

def user_register(req):
    form = Register()
    if req.method == "POST":
         form = Register(req.POST)
         if form.is_valid():
            form.save()
            return redirect("login")
         else:
             messages.error(req,"สร้างบัญชีไม่สำเร็จ")
             form = Register()
             return redirect("register")
             
    return render(req, 'Register.html',{"form":form})


def user_logout(req):
        logout(req)
        return redirect("/")



