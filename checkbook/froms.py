from django.forms import ModelForm
from .models Category
#from django import forms

class CatForm(forms.ModForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "frequency",
            "budget",
        ]
