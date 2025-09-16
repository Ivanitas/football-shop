from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm

def show_main(request):
    products = Product.objects.all()
    context = {
        'app_name': 'Football Shop',
        'name': 'Muhammad Iffan Chalif Aziz',
        'class': 'PBP-B',
        'products': products
    }
    return render(request, 'main/main.html', context)  # UBAH PATH

def view_json(request):
    data = Product.objects.all()
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

def view_xml(request):
    data = Product.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def view_json_by_id(request, id):
    data = get_object_or_404(Product, pk=id)
    json_data = serializers.serialize("json", [data])
    return HttpResponse(json_data, content_type="application/json")

def view_xml_by_id(request, id):
    data = get_object_or_404(Product, pk=id)
    xml_data = serializers.serialize("xml", [data])
    return HttpResponse(xml_data, content_type="application/xml")

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, 'main/create_product.html', {'form': form})  

def show_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'main/detail.html', {'product': product})  