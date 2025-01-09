import django_filters
from .models import *


class XTraineeFilter(django_filters.FilterSet):

    gender = django_filters.ChoiceFilter(
        choices=[("Male", "Male"), ("Female", "Female")], label="Gender"
    )

    venue = django_filters.ModelChoiceFilter(
        queryset=XVenue.objects.all(), label="Venue"
    )
    course = django_filters.ModelChoiceFilter(
        queryset=XCourse.objects.all(), label="Discipline"
    )

    class Meta:
        model = XTrainee
        fields = ["gender", "venue", "course"]
