import django_filters
from django import forms
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Champie, Level, CVenue, Course  # adjust as necessary


class DateInput(forms.DateInput):
    input_type = "date"


class ChampieFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(
        choices=[("Male", "Male"), ("Female", "Female")],
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    level = django_filters.ModelChoiceFilter(
        queryset=Level.objects.all(),
        label="Level",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    venue = django_filters.ModelChoiceFilter(
        queryset=CVenue.objects.all(),
        label="Venue",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    course = django_filters.ModelChoiceFilter(
        queryset=Course.objects.all(),
        label="Discipline",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    entry_date = DateFromToRangeFilter(
        field_name="entry_date",
        label="Entry Date (Range)",
        widget=RangeWidget(
            attrs={"type": "date", "class": "form-control"}
        ),
    )

    class Meta:
        model = Champie
        fields = ["gender", "venue", "course", "level", "entry_date"]
