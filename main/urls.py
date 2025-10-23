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
    
    # AJAX URLs
    path('ajax/products/', views.ajax_get_products, name='ajax_get_products'),
    path('ajax/create-product/', views.ajax_create_product, name='ajax_create_product'),
    path('ajax/get-product/<int:id>/', views.ajax_get_product, name='ajax_get_product'),
    path('ajax/update-product/<int:id>/', views.ajax_update_product, name='ajax_update_product'),
    path('ajax/delete-product/<int:id>/', views.ajax_delete_product, name='ajax_delete_product'),
    path('ajax/register/', views.ajax_register, name='ajax_register'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
    path('ajax/logout/', views.ajax_logout, name='ajax_logout'),
]