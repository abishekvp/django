from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = r"mongodb+srv://pro_user:AWGlmNmlRjK4VqY1@cluster0.edxis.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

django = client.django
users = django.users

def index(request):
    if request.user.is_authenticated:return redirect("dashboard")
    else:return redirect('signin')

def dashboard(request):
    return redirect('signin')

def signup(request):
    try:
        client.admin.command('ping')
        print("Connection successful!")
        return JsonResponse({"message": f"Connection successful!"})
    except Exception as e:
        print("Connection failed:", e)
        return JsonResponse({"message": f"Connection failed: {e}"})
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if username and email and password:
            user_name = users.find_one(filter={'username': username})
            user_email = users.find_one(filter={'email': email})
            if user_name is None and user_email is None:
                users.insert_one({
                    "username": username,
                    "email": email,
                    "password": password
                })
                return JsonResponse({"message": "New Data"})
            else:
                return JsonResponse({"message": "User Exist"})
    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = {
                "username": username,
                "password": password
            }
            user = users.find_one(filter=user)
            if user:
                return JsonResponse({"message": "User found"})
            else:
                return JsonResponse({"message": "User not found"})
    return render(request,'signin.html')

def signout(request):
    if request.user.is_authenticated:logout(request)
    return redirect('signin')

def test(request):
    result = {"data": "Done"}
    return JsonResponse({"code": 200, "message": "Success", "result": result})
