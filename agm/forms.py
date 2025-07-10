from django import forms
from dashboard.models import *
from .models import *



class ComisersForm(forms.ModelForm):
    class Meta:
        model = Comiser
        fields = [
            "first_name",
            "last_name",
            "comittee",
            "photo",
            "role",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "comittee": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }