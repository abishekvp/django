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

def check_user_exist(email):
    return User.objects.filter(email=email).exists()

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
            user_data = {'username':user_data['username'], 'name':user_data['name'], 'contact':user_data['contact'], 'email':user_data['email']}
            return render(request,'profile.html', {'user_data':user_data})
        except:
            messages.info(request, 'Mongo Database Error')
            return redirect('index')
    else:return redirect('signin')

@login_required(login_url='signin')
def edit_profile(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            name=request.POST.get("name")
            username = request.user.username
            contact=request.POST.get("contact")
            email = request.user.email
            db_user.find_one_and_update(filter={'username':username},update={"$set":{'username':username, 'name':name, 'contact':contact, 'email':email}})
            return redirect('profile')
        try:
            user_data = db_user.find_one(filter={'username':request.user.username})
            user_data = {'username':user_data['username'], 'name':user_data['name'], 'contact':user_data['contact'], 'email':user_data['email']}
            return render(request,'edit-profile.html', {'user_data':user_data})
        
        except:
            messages.info(request, 'Mongo Database Error')
            return redirect('index')

@login_required(login_url='signin')
def chat(request):
    if request.method == 'POST':
        msg = request.POST['name']
        return HttpResponse(msg)
    return render(request,'chat.html')

def signin(request):
    if request.method == 'POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            username=email.split('@')[0]
            if check_user_exist(email):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.info(request, 'Invalid password')
            else:
                messages.info(request, 'Email not found')
        except:
            messages.info(request, 'Error acquired on signin')  
    return render(request,'signin.html')

def signup(request):
    if request.method == 'POST':
        name=request.POST.get("su-name")
        contact=request.POST.get("su-contact")
        email=request.POST.get("su-email")
        password=request.POST.get("su-password")
        username=email.split('@')[0]
        if check_user_exist(email):
            messages.info(request, 'User already exist')
        else:
            client.django.user.insert_one({'username':username, 'name':name, 'contact':contact, 'email':email, 'password':password})
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

