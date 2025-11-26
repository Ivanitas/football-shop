from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({
                "status": True,
                "message": "Login successful!",
                "username": user.username
            })
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, check your username/password."
            }, status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
            
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
            
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "status": True,
            "message": "User created successfully!"
        })

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({
            "status": True,
            "message": "Logged out successfully!"
        })