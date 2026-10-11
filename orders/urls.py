from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('create/', views.order_create, name='create'),
    path('management/', views.order_management, name='management'),
    path('management/<int:order_id>/update/', views.order_update_status, name='update_status'),
    path('my/', views.my_orders, name='my_orders'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment/<int:order_id>/result/', views.payment_result, name='payment_result'),
]
