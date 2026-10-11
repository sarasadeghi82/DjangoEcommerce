from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from accounts.decorators import role_required
import random


def cart_add(request, product_id):
    cart = Cart(request)                                      # create cart object 
    product = get_object_or_404(Product, id=product_id)       
    cart.add(product=product)
    next_url= request.META.get('HTTP_REFERER')
    return redirect(next_url)


def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)

    next_url = request.META.get('HTTP_REFERER', 'orders:cart_detail')
    return redirect(next_url)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    next_url = request.META.get('HTTP_REFERER', 'orders:cart_detail')
    return redirect(next_url)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})



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



@login_required
def order_create(request):        # بعد از زدن کلید ثبت سفارش   create Order and OrderItem 
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
    return redirect('orders:payment', order_id=order.id)



@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_paid:
        return redirect('orders:payment_result', order_id=order.id)

    if request.method == 'POST':
        success = simulate_payment(request.POST)

        if success:
            order.is_paid = True
            order.status = 'processing'

            for item in order.items.all():
                if item.product:
                    item.product.stock-= item.quantity
                    item.product.save()

        else:
            order.status = 'Unsuccessful'              
        order.save()

        return redirect('orders:payment_result', order_id=order.id)

    return render(request, 'orders/payment.html', {'order': order})


@login_required
def payment_result(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/payment_result.html', {'order': order})



def simulate_payment(post_data):
    card_number = post_data.get('card_number', '').strip()
    if len(card_number) != 16 or not card_number.isdigit():
        return False
    return random.random() > 0.1               # عدد اعشاری بین 0 , 1 
#random.random() > 0.1  # 90% شانس موفقیت




