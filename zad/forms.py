from django import forms


class AuthForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())