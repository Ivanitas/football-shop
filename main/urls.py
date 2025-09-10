from django.urls import path
from main import views

urlpatterns = [
    path('', views.show_main, name='show_main'),
]