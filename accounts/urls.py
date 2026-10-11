from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
 
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/bypass', LoginView.as_view(template_name='accounts/baypass.html'), name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('users/', views.user_management, name='user_management'),
    path('users/<int:user_id>/update-role/', views.user_update_role, name='user_update_role'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/',PasswordChangeView.as_view(template_name='accounts/change_password.html',success_url='/accounts/change-password/done/'),name='change_password'),
    path('change-password/done/',PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'),name='password_change_done'),
]




