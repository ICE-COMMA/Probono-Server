from django import forms

class SignUpForm(forms.Form):
    ID = forms.CharField(label="User ID", max_length=100, required=True)
    name = forms.CharField(label="Name", max_length=100, required=True)
    PW = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)
    gender = forms.CharField(label="Gender", max_length=10, required=True)
    date = forms.DateField(label="Date", required=True)
    impaired = forms.CharField(label="Impaired", max_length=100, required=True)