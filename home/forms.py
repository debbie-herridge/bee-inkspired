from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

# Register new user form
class CreateUserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username','email','password1','password2']

# Booking form
class BookingForm(ModelForm):
    class Meta: 
        model = Booking
        fields = ['design','preference']

# Enquiry form
class EnquiryForm(ModelForm):
    class Meta: 
        model = Enquiry
        fields = ['enquiry','image']