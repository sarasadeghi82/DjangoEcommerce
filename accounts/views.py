from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, ProfileEditForm
from accounts.decorators import role_required, login_required
from .models import User
from django.contrib import messages



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')



@role_required('admin')
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_management.html', {'users': users})



@role_required('admin')
def user_update_role(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in dict(User.ROLE_CHOICES):
             if target_user == request.user and new_role != 'admin':
                pass  
             else :
                target_user.role = new_role
                target_user.save()
    return redirect('accounts:user_management')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات حساب شما با موفقیت به‌روزرسانی شد.')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})











