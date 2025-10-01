from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from .models import Product
from .forms import ProductForm

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
    products = Product.objects.filter(user=request.user)
    
    context = {
        'app_name': 'Cosmic Store',
        'name': 'abhiseka.susanto',
        'username': request.user.username,
        'class': 'PBP A',
        'products': products,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, 'main/main.html', context)

def view_json(request):
    data = Product.objects.filter(user=request.user)
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

def view_xml(request):
    data = Product.objects.filter(user=request.user)
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def view_json_by_id(request, id):
    data = get_object_or_404(Product, pk=id, user=request.user)
    json_data = serializers.serialize("json", [data])
    return HttpResponse(json_data, content_type="application/json")

def view_xml_by_id(request, id):
    data = get_object_or_404(Product, pk=id, user=request.user)
    xml_data = serializers.serialize("xml", [data])
    return HttpResponse(xml_data, content_type="application/xml")

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def show_detail(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    return render(request, 'main/detail.html', {'product': product})

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('main:show_main')
    
    return render(request, 'main/delete_product.html', {'product': product})