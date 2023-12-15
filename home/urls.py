from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('edit_profile/', views.EditUser.as_view(), name='edit_profile'),

    path('dashboard/', views.customerDashboard, name='customer-dashboard'),
    path('dashboard-artist/', views.artistDashboard, name='artist-dashboard'),

    path('book/', views.book, name='book'),
    path('update-booking/', views.updateBooking, name='update-booking'),
    path('enquire/', views.userEnquiry, name='enquire'),
]