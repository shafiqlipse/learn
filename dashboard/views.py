from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    context = {}
    return render(request, "dashboard/overview.html", context)



@login_required(login_url='login')
def seasons_view(request):
    user = request.user
    seasons = Season.objects.filter(status="Active").order_by('-start_date')
    new_season = None
    season_to_edit = None

    # Check if we're editing
    season_id = request.GET.get("edit") or request.POST.get("season_id")
    if season_id:
        season_to_edit = get_object_or_404(Season, id=season_id)

    if request.method == "POST":
        if season_to_edit:
            cform = SeasonForm(request.POST, request.FILES, instance=season_to_edit)
        else:
            cform = SeasonForm(request.POST, request.FILES)

        if cform.is_valid():
            new_season = cform.save(commit=False)
            if not season_to_edit:  # Only set these when creating
                new_season.added_by = user
            new_season.save()
            return redirect("seasons")
    else:
        if season_to_edit:
            cform = SeasonForm(instance=season_to_edit)
        else:
            cform = SeasonForm()

    context = {
        "seasons": seasons,
        "cform": cform,
        "season_to_edit": season_to_edit,
    }

    return render(request, "elements/seasons.html", context)



@login_required(login_url='login')
def venues_view(request):
    user = request.user
    venues = Venue.objects.filter(status="Active")
    new_venue = None
    venue_to_edit = None

    # Check if we're editing
    venue_id = request.GET.get("edit") or request.POST.get("venue_id")
    if venue_id:
        venue_to_edit = get_object_or_404(Venue, id=venue_id)

    if request.method == "POST":
        if venue_to_edit:
            cform = VenueForm(request.POST, request.FILES, instance=venue_to_edit)
        else:
            cform = VenueForm(request.POST, request.FILES)

        if cform.is_valid():
            selected_courses = cform.cleaned_data["courses"]
            new_venue = cform.save(commit=False)
            if not venue_to_edit:  # Only set these when creating
                new_venue.added_by = user
                
            new_venue.save()
            new_venue.courses.set(selected_courses)
            return redirect("venues")
    else:
        if venue_to_edit:
            cform = VenueForm(instance=venue_to_edit)
        else:
            cform = VenueForm()

    context = {
        "venues": venues,
        "cform": cform,
        "venue_to_edit": venue_to_edit,
    }

    return render(request, "elements/venues.html", context)

@login_required(login_url='login')
def courses_view(request):
    user = request.user
    courses = Course.objects.all()
    new_course = None
    course_to_edit = None

    # Check if we're editing
    course_id = request.GET.get("edit") or request.POST.get("course_id")
    if course_id:
        course_to_edit = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        if course_to_edit:
            cform = CourseForm(request.POST, request.FILES, instance=course_to_edit)
        else:
            cform = CourseForm(request.POST, request.FILES)

        if cform.is_valid():
            
            new_course = cform.save(commit=False)
            if not course_to_edit:  # Only set these when creating
                new_course.added_by = user
                
            new_course.save()
            return redirect("courses")
    else:
        if course_to_edit:
            cform = CourseForm(instance=course_to_edit)
        else:
            cform = CourseForm()

    context = {
        "courses": courses,
        "cform": cform,
        "course_to_edit": course_to_edit,
    }

    return render(request, "elements/courses.html", context)