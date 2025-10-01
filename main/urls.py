from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('json/', views.view_json, name='view_json'),
    path('xml/', views.view_xml, name='view_xml'),
    path('json/<int:id>/', views.view_json_by_id, name='view_json_by_id'),
    path('xml/<int:id>/', views.view_xml_by_id, name='view_xml_by_id'),
    path('create/', views.create_product, name='create_product'),
    path('detail/<int:id>/', views.show_detail, name='show_detail'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
]