from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
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
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            }, status=400)

@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            
            if not username or not password1 or not password2:
                return JsonResponse({
                    "status": False,
                    "message": "All fields are required."
                }, status=400)
            
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
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            }, status=400)

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({
            "status": True,
            "message": "Logged out successfully!"
        })

@csrf_exempt
def api_check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "status": True,
            "username": request.user.username
        })
    else:
        return JsonResponse({
            "status": False,
            "message": "Not authenticated"
        }, status=401)