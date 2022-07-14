from django import forms
from MyKart.models import *




class RegistrationForm(forms.ModelForm):

    class Meta:
        model=Customer
        fields='__all__'
        exclude=('password','walletbalance','phone')