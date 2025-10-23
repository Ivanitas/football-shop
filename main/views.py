from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Product
from .forms import ProductForm

# AJAX REGISTER
@csrf_exempt
def ajax_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserCreationForm(data)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({
                    'success': True, 
                    'message': 'Registration successful!',
                    'redirect_url': '/'
                })
            else:
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({
                    'success': False, 
                    'message': 'Registration failed',
                    'errors': errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': str(e)
            })
    return JsonResponse({'success': False, 'message': 'Invalid method'})

# AJAX LOGIN
@csrf_exempt
def ajax_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = AuthenticationForm(request, data=data)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                response = JsonResponse({
                    'success': True, 
                    'message': 'Login successful!',
                    'redirect_url': '/'
                })
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid username or password'
                })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': str(e)
            })
    return JsonResponse({'success': False, 'message': 'Invalid method'})

# AJAX LOGOUT
@login_required
@csrf_exempt
def ajax_logout(request):
    if request.method == 'POST':
        logout(request)
        response = JsonResponse({
            'success': True, 
            'message': 'Logout successful!',
            'redirect_url': '/login/'
        })
        response.delete_cookie('last_login')
        return response
    return JsonResponse({'success': False, 'message': 'Invalid method'})

# Traditional views for fallback
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect('main:show_main')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def show_main(request):
    context = {
        'app_name': 'Football Shop',
        'name': 'Muhammad Iffan Chalif Aziz',
        'username': request.user.username,
        'class': 'PBP B',
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, 'main/main.html', context)

# AJAX PRODUCT VIEWS
@login_required
@csrf_exempt
def ajax_get_products(request):
    try:
        products = Product.objects.filter(user=request.user)
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'category': product.category,
                'stock': product.stock,
                'brand': product.brand,
                'thumbnail': product.thumbnail,
                'is_featured': product.is_featured,
                'date_added': product.date_added.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'success': True, 'products': products_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@csrf_exempt
def ajax_create_product(request):
    if request.method == 'POST':
        try:
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                return JsonResponse({'success': True, 'message': 'Product created successfully!'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid form data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def ajax_get_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id, user=request.user)
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category,
            'stock': product.stock,
            'brand': product.brand,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
        }
        return JsonResponse({'success': True, 'product': product_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@csrf_exempt
def ajax_update_product(request, id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=id, user=request.user)
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid form data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def ajax_delete_product(request, id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=id, user=request.user)
            product.delete()
            return JsonResponse({'success': True, 'message': 'Product deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# TRADITIONAL PRODUCT VIEWS
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, 'main/create_product.html', {'form': form})

def view_json(request):
    data = Product.objects.filter(user=request.user)
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

def view_xml(request):
    data = Product.objects.filter(user=request.user)
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

# TAMBAHKAN FUNGSI YANG HILANG INI
def view_json_by_id(request, id):
    data = get_object_or_404(Product, pk=id, user=request.user)
    json_data = serializers.serialize("json", [data])
    return HttpResponse(json_data, content_type="application/json")

def view_xml_by_id(request, id):
    data = get_object_or_404(Product, pk=id, user=request.user)
    xml_data = serializers.serialize("xml", [data])
    return HttpResponse(xml_data, content_type="application/xml")

def show_detail(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    return render(request, 'main/detail.html', {'product': product})

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('main:show_main')
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/edit_product.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('main:show_main')
    return render(request, 'main/delete_product.html', {'product': product})