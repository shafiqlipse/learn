from django import forms
from .models import *


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = [
            "name",
            "start_date",
            "year",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            "name",
            "season",
            "courses",
        ]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Filter the championship queryset to only include active championships
            self.fields['season'].queryset = Season.objects.filter(status='Active')
            
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "season": forms.Select(attrs={"class": "form-control"}),
            "courses": forms.SelectMultiple(attrs={"class": "form-control js-example-basic-multiple-name"}),
        }
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "name",
            "level",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
        }
class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = [
            "name",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }   