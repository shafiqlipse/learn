from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def school_required(view_func):
    @login_required(login_url="login")
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_trainer:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "auth/login.html")  # You can customize this template

    return _wrapped_view


def admin_required(login_url="login"):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=login_url)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "login.html")  # You can customize this template

        return _wrapped_view

    return decorator


# def transfer_required(login_url="login"):
#     def decorator(view_func):
#         @wraps(view_func)
#         @login_required(login_url=login_url)
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.is_tech:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return render(request, "login.html")  # You can customize this template

#         return _wrapped_view

#     return decorator


def staff_required(view_func):
    @login_required(login_url="login")
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "login.html")  # You can customize this template

    return _wrapped_view


def anonymous_required(view_func):
    """
    Decorator to ensure that the view is only accessible to anonymous users (not logged in).
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if the user is an admin
            if (
                request.user.is_staff or request.user.is_superuser
            ):  # Adjust as per your admin definition
                return redirect(
                    "dashboard"
                )  # Admin users are redirected to overview
            else:
                return redirect(
                    "dashboard/profile.html"
                )  # Regular users are redirected to profile
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view
