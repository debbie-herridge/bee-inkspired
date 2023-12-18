import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users

def home(request):
    """
    Simple view to render homepage.
    """
    reviews = Review.objects.all()
    context = {
        'reviews':reviews,
    }
    return render(request, 'index.html', context)

def gallery(request):
    """
    Simple view to render gallery.
    """
    return render(request, 'gallery.html')

@unauthenticated_user
def register(request):
    """
    Create new user by registration form and adding them to customer group.
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return redirect('login')
        else:
            messages.error(request, 'Registration failed, please ensure you are filling in all the fields. Alternatively try refresh and try again')
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    """
    Authenticate login details and sign users in.
    """
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

def logoutUser(request):
    """
    Simple view to log out user.
    """
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerDashboard(request):
    """
    Display customer dashboard with signed in users information
    """
    today = datetime.datetime.today()
    bookings = Booking.objects.filter(customer=request.user).filter(date__gte=today).order_by('date')
    previous_booking = Booking.objects.filter(customer=request.user).exclude(date__gte=today).order_by('date')
    context = {
        'bookings':bookings,
        'previous_booking':previous_booking,
    }
    return render(request, 'dashboard-user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def artistDashboard(request):
    """
    Display artist dashboard with all upcoming bookings and enquires.
    """
    today = datetime.datetime.today()
    bookings = Booking.objects.all().filter(date__gte=today).order_by('date')
    total_bookings = bookings.count()
    enquiry = Enquiry.objects.all()
    enquiry_bookings = enquiry.count()
    context = {
        'bookings':bookings, 
        'total_bookings':total_bookings,
        'enquiry':enquiry,
        'enquiry_bookings':enquiry_bookings,
    }
    return render(request, 'dashboard-artist.html', context)

def week(days):
    """
    Function to return the available dates.
    """
    dates_list = []
    unavailable = []
    start = datetime.datetime.today()
    booked = Booking.objects.values_list('date', flat=True)

    # For loop to get the a list of days
    for day in range(0,days):
        dates_list.append((start + datetime.timedelta(days=day)).strftime('%a %d %b %Y'))

    # Create a list of the booked dates
    for slot in booked:
        booked_slot = slot.strftime('%a %d %b %Y')
        unavailable.append(booked_slot)

    # Remove booked dates from list of upcoming days
    for i in unavailable:
        try:
            dates_list.remove(i)
        except ValueError:
            pass

    return dates_list

@login_required
def book(request):
    """
    Save user booking form and send data to customer dashboard.
    """
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

@login_required
def updateBooking(request, pk):
    """
    Allow users to update their specific booking.
    """
    booking = get_object_or_404(Booking, pk=pk)
    dates = week(14)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
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
        form = BookingForm(instance=booking)
    context = {
        'form':form,
        'dates':dates,
        'booking':booking,
    }
    return render(request, 'update-booking.html', context)

@login_required
def cancelBooking(request, pk):
    """
    Allow users to cancel a specific booking.
    """
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('customer-dashboard')
    else:
        print('form not valid')
    context = {
        'booking':booking,
    }
    return render(request, 'cancel-booking.html', context)

@login_required
def userEnquiry(request):
    """
    Allow users to send a reference image with enquiry.
    """
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

@login_required
def deleteEnquiry(request, pk):
    """
    Allow admin to delete an enquiry when dealt with.
    """
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        return redirect('artist-dashboard')
    else:
        print('form not valid')
        print(enquiry.errors)
    context = {
        'enquiry':enquiry,
    }
    return render(request, 'delete-enquiry.html', context)

@login_required
def reviewForm(request, pk):
    """
    Form for users to review previous appointments.
    """
    if request.method == 'POST':
        form = UserReview(request.POST)
        booking = get_object_or_404(Booking, pk=pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.save()
            print(booking)
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
