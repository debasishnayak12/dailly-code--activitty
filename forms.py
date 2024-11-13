from django import forms
from .models import user

class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['id','name', 'mobile']
