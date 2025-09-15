from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

