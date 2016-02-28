from django import forms
from .models import Sales


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=128)
    pw = forms.CharField(label='Password', widget=forms.PasswordInput)

#
# class AddForm(forms.ModelForm):
#     class Meta:
#         model = Sales
#         fields()
#

