from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sliders/', views.slider_management, name='slider_management'),
    path('sliders/add/', views.slider_create, name='slider_create'),
    path('sliders/<int:pk>/edit/', views.slider_edit, name='slider_edit'),
    path('sliders/<int:pk>/delete/', views.slider_delete, name='slider_delete'),
]



