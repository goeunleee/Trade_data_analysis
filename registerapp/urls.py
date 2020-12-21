from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('join/', views.join, name='join'),
    path('logout/', views.logout, name='logout'),
    path('agreement/', views.agreement, name='agreement'),
    path('registerauth/', views.join_success, name='join_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

]