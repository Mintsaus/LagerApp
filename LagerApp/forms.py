from django import forms
from django.forms import ModelForm
from .models import Transactions


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=128)
    pw = forms.CharField(label='Password', widget=forms.PasswordInput)




class AddForm(ModelForm):

    class Meta:
        model = Transactions
        fields = ['date', 'product', 'warehouse', 'quantity']
        widgets = {'date': forms.DateInput(attrs={'class': 'datepicker'})}


