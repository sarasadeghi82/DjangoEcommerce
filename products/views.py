from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Brand
from accounts.decorators import role_required, login_required
from orders.cart import Cart
from django.core.exceptions import PermissionDenied



def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get('category')      # query string   { 'category' = 'laptop' }
    if category_slug: 
        products = products.filter(category__slug=category_slug) # objects's field's field 

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart_quantity = cart.get_quantity(product)
    context = {'product': product , 'cart_quantity': cart_quantity }
    return render(request, 'products/product_detail.html', context)



@role_required('admin', 'staff')
def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            category_id=request.POST.get('category') or None,        # '' or None 
            brand_id=request.POST.get('brand') or None,
            price=request.POST.get('price'),
            stock=request.POST.get('stock') or 0,
            description=request.POST.get('description', ''),
            image=request.FILES.get('image'),
            created_by=request.user,
        )
        return redirect('products:list')

    context = {'categories': Category.objects.all(), 'brands': Brand.objects.all()}
    return render(request, 'products/product_form.html', context)



@role_required('admin', 'staff')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category') or None
        product.brand_id = request.POST.get('brand') or None
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock') or 0
        product.description = request.POST.get('description', '')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('products:list')

    context = {'product': product, 'categories': Category.objects.all(), 'brands': Brand.objects.all()}
    return render(request, 'products/product_form.html', context)



@role_required('admin', 'staff')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products:list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart_quantity = cart.get_quantity(product)
    context = {'product': product, 'cart_quantity': cart_quantity}
    return render(request, 'products/product_detail.html', context)







