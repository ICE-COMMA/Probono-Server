from django import forms
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'name', 'password', 'sex', 'birth', 'disability', 'custom']
        widgets = {
            'password': forms.PasswordInput(),
        }