from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
     path('base2/', views.user_page, name='user_page'),
     path('register_user/', views.register_user, name='register_user'),
     path('admin_view/',views.admin_page,name='admin_page'),
     path('login/', views.login_user, name='login_user'),
     path('products/add/', views.add_product, name='add_product'),
     path('products/', views.product_list, name='product_list'),
     path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
     path('logout/', views.logout_view, name='logout'),
     path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
     path('products/<int:pk>/', views.product_detail, name='product_detail'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.cart, name='cart'),
     path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
     path('delete/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
     path('checkout/', views.checkout_view, name='checkout'),
     path('order_confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
     path('order_history/', views.order_history, name='order_history'),
     path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
