from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('dashboard/', views.customerDashboard, name='customer-dashboard'),
    path('dashboard-artist/', views.artistDashboard, name='artist-dashboard'),
]