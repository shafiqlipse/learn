from django import forms
from dashboard.models import *
from .models import *


class ChampiesForm(forms.ModelForm):
    class Meta:
        model = Champie
        fields = [
            "first_name",
            "last_name",
            "venue",
            "championship",
            "photo",
            "contact",
            "course",
            "gender",
            "date_of_birth",
            "place",
            "designation",
            "level",
        ]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Filter the championship queryset to only include active championships
            self.fields['championship'].queryset = Championship.objects.filter(status='Active')

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "championship": forms.Select(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
          
            "place": forms.TextInput(attrs={"class": "form-control"}),
           
            "venue": forms.Select(attrs={"class": "form-control"}),
           
            "designation": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),

            "gender": forms.Select(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
