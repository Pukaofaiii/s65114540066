from django import forms
from .models import User_Profile

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']