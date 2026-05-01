import django_filters
from django import forms
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import *


class ComiserFilter(django_filters.FilterSet):

    comittee = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Discipline",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    role = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Role",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Comiser
        fields = [ "comittee", "role"]
