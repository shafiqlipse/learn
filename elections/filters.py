import django_filters
from django import forms
from .models import *


class ResultsFilter(django_filters.FilterSet):

    gender = django_filters.ChoiceFilter(
        field_name="candidate__user__gender",
        choices=[("Male", "Male"), ("Female", "Female")],
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    candidate = django_filters.ModelChoiceFilter(
        queryset=Candidate.objects.select_related("school"),
        label="Candidate",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    election = django_filters.ModelChoiceFilter(
        queryset=Election.objects.all(),
        label="Election",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    level = django_filters.ChoiceFilter(
        field_name="election__level",
        choices=ElectionLevel.choices,
        label="Level",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    result_code = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Result Code",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    is_elected = django_filters.BooleanFilter(label="Elected")

    min_votes = django_filters.NumberFilter(field_name="votes", lookup_expr="gte")
    max_votes = django_filters.NumberFilter(field_name="votes", lookup_expr="lte")

    class Meta:
        model = Result
        fields = [
            "candidate", "election",
            "result_code", "is_elected"
        ]

# class ElectionFilter(django_filters.FilterSet):
    
#     level = django_filters.ChoiceFilter(
#         field_name="level",
#         choices=[("Male", "Male"), ("Female", "Female")],
#         label="Level",
#         widget=forms.Select(attrs={"class": "form-control"})
#     )
    
#     position = django_filters.ChoiceFilter(
#         field_name="candidate__user__gender",
#         choices=[("Male", "Male"), ("Female", "Female")],
#         label="Gender",
#         widget=forms.Select(attrs={"class": "form-control"})
#     )
    
#     district = django_filters.ModelChoiceFilter(
#         field_name="election__district",
#         queryset=District.objects.all(),
#         label="District",
#         widget=forms.Select(attrs={"class": "form-control"})
#     )

#     zone = django_filters.ModelChoiceFilter(
#         field_name="election__zone",
#         queryset=Zone.objects.all(),
#         label="Zone",
#         widget=forms.Select(attrs={"class": "form-control"})
#     )

#     region = django_filters.ModelChoiceFilter(
#         field_name="election__region",
#         queryset=Region.objects.all(),
#         label="Region",
#         widget=forms.Select(attrs={"class": "form-control"})
#     )



#     class Meta:
#         model = Election
#         fields = ["gender", "level", "candidate", "election", "result_code"]
