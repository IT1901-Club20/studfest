"""Form-class for manager_edit.html"""
from django import forms

class needsForm(forms.Form):
    """Adds needed form-fields, except hidden values (concertId etc). """
    newNeeds = forms.CharField(max_length=24, min_length=1, label="New requirements")
