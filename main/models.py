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

@receiver(post_migrate)
def create_default_products(sender, **kwargs):
    if sender.name == 'main':
        if not Product.objects.exists():
            Product.objects.create(
                name="Football Jersey",
                price=79,
                description="High-quality football jersey with moisture-wicking technology.",
                thumbnail="https://via.placeholder.com/300x400?text=Jersey",
                category="Jerseys",
                is_featured=True,
                stock=50,
                brand="Nike"
            )
            Product.objects.create(
                name="Football Boots",
                price=129,
                description="Professional football boots with enhanced grip and comfort.",
                thumbnail="https://via.placeholder.com/300x400?text=Boots",
                category="Footwear",
                is_featured=True,
                stock=30,
                brand="Adidas"
            )
            print("Default products created!")