from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from accounts.decorators import role_required


def cart_add(request, product_id):
    cart = Cart(request)                                      # create cart object 
    product = get_object_or_404(Product, id=product_id)       
    cart.add(product=product)
    return redirect('orders:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})


@login_required
def order_create(request):        # create order and orderItem objects 
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('orders:cart_detail')

    order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
        )
    cart.clear()
    return render(request, 'orders/order_success.html', {'order': order})



@role_required('admin', 'staff')
def order_management(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/order_management.html', {'orders': orders})


@role_required('admin', 'staff')
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return  redirect('orders:management')



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


