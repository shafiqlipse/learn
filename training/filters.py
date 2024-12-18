import django_filters
from .models import *


class TraineeFilter(django_filters.FilterSet):

    gender = django_filters.ChoiceFilter(
        choices=[("Male", "Male"), ("Female", "Female")], label="Gender"
    )
    
    level = django_filters.ModelChoiceFilter(
        queryset=Level.objects.all(), label="Level"
    )
    venue = django_filters.ModelChoiceFilter(
        queryset=Venue.objects.all(), label="Venue"
    )
    course = django_filters.ModelChoiceFilter(
        queryset=Course.objects.all(), label="Discipline"
    )

    class Meta:
        model = Trainee
        fields = ["gender", "venue", "course",  "level"]
