from django.shortcuts import render
from .models import Product

def show_main(request):
    products = Product.objects.all()
    
    context = {
        'app_name': 'Football Shop',
        'name': 'Muhammad Iffan Chalif Aziz',  
        'class': 'PBP-B',  
        'products': products
    }
    
    return render(request, 'main.html', context)