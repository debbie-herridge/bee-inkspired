from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.views import generic
from django.urls import reverse_lazy
import datetime

from .models import * 
from .forms import *
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
def home(request):
    reviews = Review.objects.all()
    context = {
        'reviews':reviews,
    }
    return render(request, 'index.html', context)

def gallery(request):
    return render(request, 'gallery.html')

# Register new user
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
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

class EditUser(generic.UpdateView):
    """
    Edit signed in users information
    """
    form_class = EditUserProfile
    template_name = "edit-user.html"
    success_url = reverse_lazy('customer-dashboard')

    def get_object(self):
        return self.request.user

# User dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerDashboard(request):
    today = datetime.datetime.today()
    bookings = Booking.objects.filter(customer=request.user).filter(date__gte=today).order_by('date')
    previous_booking = Booking.objects.filter(customer=request.user).exclude(date__gte=today).order_by('date')
    context = {
        'bookings':bookings,
        'previous_booking':previous_booking,
    }
    return render(request, 'dashboard-user.html',context)

# Artist dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def artistDashboard(request):
    today = datetime.datetime.today()
    bookings = Booking.objects.all().filter(date__gte=today).order_by('date')
    enquiry = Enquiry.objects.all()
    total_bookings = bookings.count()
    enquiry_bookings = enquiry.count()

    context = {
        'bookings':bookings, 
        'total_bookings':total_bookings,
        'enquiry':enquiry,
        'enquiry_bookings':enquiry_bookings,
    }
    return render(request, 'dashboard-artist.html', context)

# Put next 14 days into a list and remove booked dates
def week(days):
    dates_list = []
    unavailable = []
    start = datetime.datetime.today()
    booked = Booking.objects.values_list('date', flat=True)

    for day in range(0,days):
        dates_list.append((start + datetime.timedelta(days=day)).strftime('%a %d %b %Y'))
        
    for slot in booked:
        booked_slot = slot.strftime('%a %d %b %Y')
        unavailable.append(booked_slot)

    for i in unavailable:
        try:
            dates_list.remove(i)
        except ValueError:
            pass

    return dates_list


# Booking flash design appointment page
@login_required
def book(request):
    designs = Design.objects.all()
    dates = week(14)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user

            # Change date back into strptime to save onto booking model
            date_object = request.POST['date']
            booking.date = datetime.datetime.strptime(date_object, '%a %d %b %Y').date()

            booking.save()
            return redirect('customer-dashboard')
        else:
            print('form not valid')
            print(form.errors)

    else:
        form = BookingForm()

    context = {
        'form':form,
        'dates':dates,
        'designs':designs,
    }  

    return render(request, 'book.html', context)

# update booking
@login_required
def updateBooking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    dates = week(14)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
                        
            date_object = request.POST['date']
            booking.date = datetime.datetime.strptime(date_object, '%a %d %b %Y').date()

            booking.save()

            return redirect('customer-dashboard')
    else:
        form = BookingForm(instance=booking)
    context = {
        'form':form,
        'dates':dates,
        'booking':booking,
    }
    return render(request, 'update-booking.html', context)

# cancel booking
@login_required
def cancelBooking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('customer-dashboard')
    context = {
        'booking':booking,
    }
    return render(request, 'cancel-booking.html', context)

# Send an enquiry
@login_required
def userEnquiry(request):
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST, request.FILES)
        if form.is_valid():

            enquiry = form.save(commit=False)
            enquiry.customer = request.user
            enquiry.save()

            messages.success(request, 'Thank you, your enquiry has been sent and Olivia will be in touch as soon as possible!')
            return render(request, 'enquiry-success.html')
        else:
            print('form not valid')
            print(enquiry.errors)
    context = {
        'form':form,
    }
    return render(request, 'enquire.html', context)

# Delete an enquiry
@login_required
def deleteEnquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        return redirect('artist-dashboard')
    context = {
        'enquiry':enquiry,
    }
    return render(request, 'delete-enquiry.html', context)


# Booking flash design appointment page
@login_required
def reviewForm(request):
    if request.method == 'POST':
        form = UserReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.save()
            return redirect('customer-dashboard')
        else:
            print('form not valid')
            print(form.errors)
    else:
        form = UserReview()

    context = {
        'form':form,
    }  

    return render(request, 'review-form.html', context)