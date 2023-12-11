from django.http import HttpResponse
from django.shortcuts import redirect

# Check if user is logged in to stop login or register page showing
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('home')
        else: 
            return view_func(request, *args, **kwargs)
    return wrapper_func
