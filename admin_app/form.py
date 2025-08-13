from django import forms

from form_service.models import ModelForm

class UserService(forms.ModelForm):
    class Meta:
        model = ModelForm
        fields = ['first_name', 'last_name','email','phone_number','Laundry','clothes','number_clothes','number_baskets','admin_price']