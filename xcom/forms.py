from django import forms
from dashboard.models import *
from .models import *


class XTraineesForm(forms.ModelForm):
    class Meta:
        model = XTrainee
        fields = [
            "first_name",
            "last_name",
            "venue",
           
            "photo",
            "contact",
            "course",
            "email",
            "district",
            "gender",
            "date_of_birth",
            "place",
            
        
            
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "tid": forms.NumberInput(attrs={"class": "form-control"}),
            "venue": forms.Select(attrs={"class": "form-control"}),
           
        
            "course": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
           
           
            "gender": forms.Select(attrs={"class": "form-control"}),
          
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
