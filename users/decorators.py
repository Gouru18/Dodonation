"""
from django.shortcuts import redirect
from functools import wraps

def login_required_home(view_func):
   
    Custom decorator that redirects unauthenticated users to home instead of login.
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        # Unauthenticated users
        if not user.is_authenticated:
            return redirect('homepage')
        # NGO not verified
        if user.role == 'ngo' and not user.is_verified:
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper
"""
    
from django.shortcuts import redirect
from functools import wraps

def login_required_home(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('homepage')
        if user.role == 'ngo':
            ngo_profile = getattr(user, "ngo_profile", None)
            if not ngo_profile or not ngo_profile.is_validated or not ngo_profile.is_confirmed:
                return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper