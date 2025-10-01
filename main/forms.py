from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'brand', 'thumbnail', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter product description...'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Electronics, Clothing...'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name...'}),
            'thumbnail': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price ($)',
            'category': 'Category',
            'stock': 'Stock Quantity',
            'brand': 'Brand',
            'thumbnail': 'Image URL',
            'is_featured': 'Featured Product',
        }