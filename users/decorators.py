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
            # Require that NGO has a profile, but do not check `is_validated`.
            if not ngo_profile:
                return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_ngo(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('homepage')
        if request.user.role != 'ngo':
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_donor(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('homepage')
        if request.user.role != 'donor':
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper