from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    thumbnail = models.URLField()
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)  
    
    def __str__(self):
        return self.name