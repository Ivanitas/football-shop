from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)  # atribut tambahan
    brand = models.CharField(max_length=100, blank=True)  # atribut tambahan
    
    def __str__(self):
        return self.name
