from django.shortcuts import render
from .models import Product

def show_main(request):
    products = Product.objects.all()
    
    context = {
        'app_name': 'Football Shop',
        'name': 'Nama Anda',  # Ganti dengan nama Anda
        'class': 'Kelas Anda',  # Ganti dengan kelas Anda
        'products': products
    }
    
    return render(request, 'main.html', context)