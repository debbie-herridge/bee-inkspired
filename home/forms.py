from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import *

# Register new user form
class CreateUserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2']

class EditUserProfile(UserChangeForm):
    """
    Handles new details for existing users.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Update your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Update your last name'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Update your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Update your email address'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email']

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

class UserReview(ModelForm):
    class Meta: 
        model = Review
        fields = ['rating','recommend', 'review']