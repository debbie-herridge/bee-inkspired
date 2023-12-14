from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

from .models import * 
from .forms import *
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
def home(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

# Register new user
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Welcome to the family ' + user)
            return redirect('login')
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

# Login user
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('artist-dashboard')
            else:
                return redirect('customer-dashboard')
        else:
            messages.info(request, 'Username or password is invalid')
    context = {
    }
    return render(request, 'login.html', context)

# Logout user
def logoutUser(request):
    logout(request)
    return redirect('login')


# User dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerDashboard(request):
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings':bookings,
    }
    return render(request, 'dashboard-user.html',context)

# Artist dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def artistDashboard(request):
    bookings = Booking.objects.all()
    total_bookings = bookings.count()

    context = {
        'bookings':bookings, 
        'total_bookings':total_bookings,
    }
    return render(request, 'dashboard-artist.html', context)

# Put next 14 days into a list
def week(days):
    dates_list = []
    start = datetime.datetime.today()
    for day in range(0,days):
        dates_list.append((start + datetime.timedelta(days=day)).strftime('%d-%m-%y'))
    return dates_list

# Booking flash design appointment page
@login_required
def book(request):
    designs = Design.objects.all()
    dates = week(14)
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-dashboard')

    context = {
        'form':form,
        'dates':dates,
        'designs':designs,
    }
    return render(request, 'book.html', context)