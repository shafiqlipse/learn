import django_filters
from django_filters import DateFromToRangeFilter
from django import forms
from .models import XTrainee, XVenue, XCourse

class DateInput(forms.DateInput):
    input_type = "date"

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
    entry_date = DateFromToRangeFilter(
        field_name="entry_date",
        label="Entry Date (Range)",
        widget=django_filters.widgets.RangeWidget(
            attrs={"type": "date", "class": "date-input"}
        ),
    )

    class Meta:
        model = XTrainee
        fields = ["gender", "venue", "course", "entry_date"]
