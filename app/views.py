
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

def index(request):
    if request.user.is_authenticated:return redirect("dashboard")
    else:return redirect('signin')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        return redirect('signin')

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if username and email and password:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Username or Email already exists')
                return redirect('signin')
        else:
            messages.error(request, 'Please fill all the fields to create an account')
    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials Please try again')
    return render(request,'signin.html')

def signout(request):
    if request.user.is_authenticated: logout(request)
    return redirect('signin')
