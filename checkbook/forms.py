#from django.forms import ModelForm
from django import forms
from .models import Category

class AddBills(forms.Form):
    """
    Form representing a add bill transaction.
    """
    check_type = (('CR', 'credit'),('DR', 'debit'),('SV', 'savings'),('DT', 'debt reduction'),)

    dater = forms.DateField(label='Date', help_text=' .the date of the transaction')
    type = forms.ChoiceField(choices=check_type, help_text=' .credit or debit')
    category = forms.ModelChoiceField(Category.objects.values('name').distinct(), empty_label=None)
    name = forms.CharField(max_length=100, help_text=' .description')
    amount = forms.IntegerField(help_text=' .amount')
    cleared = forms.BooleanField(help_text=' .cleared with the bank?')
    addagain = forms.BooleanField(label='Add again', help_text=' .create a re-occuring bill?')
