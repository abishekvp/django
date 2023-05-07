from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# mongodb_username = 'abiraj'
# mongodb_passcode = 'MZJAgsSUQTGIiCZ1'

client = MongoClient("mongodb+srv://abiraj:MZJAgsSUQTGIiCZ1@cluster0.9md8ukt.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db_user = client.django.user

def check_user_exist(value):
    if '@' in value:
        return User.objects.filter(email=value).exists()
    elif '@' not in value:
        return User.objects.filter(username=value).exists()

@login_required(login_url='signin')
def index(request):
    if(request.user.is_authenticated):
        return render(request,'index.html')
    else:return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    if(request.user.is_authenticated):
        try:
            user_data = db_user.find_one(filter={'username':request.user.username})
            user_data = {'username':user_data['username'], 'username':user_data['username'], 'contact':user_data['contact'], 'email':user_data['email']}
            return render(request,'profile.html', {'user_data':user_data})
        except:
            messages.info(request, 'Mongo Database Error')
            return redirect('index')
    else:
        return redirect('signin')

@login_required(login_url='signin')
def edit_profile(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            username = request.POST.get("su-username")
            email=request.POST.get("su-email")
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            
            user = User.objects.get(username=request.user.username)
            client.django.user.delete_one(filter={'username':request.user.username})
            user.delete()

            client.django.user.insert_one({'username':username, 'contact':contact, 'email':email, 'password':password})
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        else:
            try:
                user_data = db_user.find_one(filter={'username':request.user.username})
                user_data = {'username':user_data['username'], 'contact':user_data['contact'], 'email':user_data['email']}
                return render(request,'edit-profile.html', {'user_data':user_data})
            except:
                messages.info(request, 'Mongo Database Error')
                return redirect('index')

def email(request):
    email=request.POST.get("email")
    if User.objects.filter(email=email).exists():
        return HttpResponse('Email-ID already exists')
    else:
        return HttpResponse('')
    
def username(request):
    username=request.POST.get("name").lower()
    if username=="":
        return HttpResponse('')
    elif username.isalnum()==False:
        return HttpResponse('Invalid Username')
    elif User.objects.filter(username=username).exists():
        return HttpResponse('Username already exists')
    else:
        return HttpResponse('')
    
def signin(request):
    if request.method == 'POST':
        p_key=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user = authenticate(request, username=p_key, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        except:pass
        try:
            user = authenticate(request, email=p_key, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        except:
            messages.info(request, 'user not found')  
    return render(request,'signin.html')

def signup(request):
    if request.method == 'POST':
        username=request.POST.get("su-username")
        contact=request.POST.get("su-contact")
        email=request.POST.get("su-email")
        password=request.POST.get("su-password")
        if check_user_exist(email):
            messages.info(request, 'User already exist')
        else:
            client.django.user.insert_one({'username':username, 'contact':contact, 'email':email, 'password':password})
            User.objects.create_user(username=username, email=email, password=password)
            if check_user_exist(email):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')

    return render(request,'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

