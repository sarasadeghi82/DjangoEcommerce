from django.shortcuts import render,redirect, get_object_or_404
from .models import Slider
from .forms  import SliderForm
from products.models import Product
from accounts.decorators import role_required



def home(request):
    sliders = Slider.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:8]
    context = {
        'sliders': sliders,
        'products': latest_products,
    }
    return render(request, 'core/home.html', context)


@role_required('admin')
def slider_management(request):
    sliders = Slider.objects.all()
    return render(request, 'core/slider_management.html', {'sliders': sliders})




@role_required('admin')
def slider_create(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:slider_management')
    else:
        form = SliderForm()
    return render(request, 'core/slider_form.html', {'form': form})



@role_required('admin')
def slider_edit(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            return redirect('core:slider_management')
    else:
        form = SliderForm(instance=slider)
    return render(request, 'core/slider_form.html', {'form': form})



@role_required('admin')
def slider_delete(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        return redirect('core:slider_management')
    return render(request, 'core/slider_confirm_delete.html', {'slider': slider})