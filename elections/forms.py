from django import forms
from dashboard.models import *
from .models import *



class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = [
            "name",
            "level",
            "position",
            "district",
            "zone",
            "region",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
            "zone": forms.Select(attrs={"class": "form-control"}),
            "region": forms.Select(attrs={"class": "form-control"}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            "fname",
            "lname",
            "gender",
            "title",
            "school",
            
        ]
        widgets = {
            "fname": forms.TextInput(attrs={"class": "form-control"}),
            "lname": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "title": forms.Select(attrs={"class": "form-control"}),
            "school": forms.Select(attrs={"class": "form-control"}),
            }


class ResultsForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "candidate",
            "votes",
            "position",

        ]
        widgets = {
            "candidate": forms.Select(attrs={"class": "form-control"}),
            "votes": forms.NumberInput(attrs={"class": "form-control"}),
            "position": forms.NumberInput(attrs={"class": "form-control"}),
            }