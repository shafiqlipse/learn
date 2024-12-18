from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    context = {}
    return render(request, "dashboard/overview.html", context)
