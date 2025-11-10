from django.shortcuts import redirect
from functools import wraps

def login_required_home(view_func):
    """
    Custom decorator that redirects unauthenticated users to home instead of login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        # Unauthenticated users
        if not user.is_authenticated:
            return redirect('home')
        # NGO not verified
        if user.role == 'ngo' and not user.is_verified:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
