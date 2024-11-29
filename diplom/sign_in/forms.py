from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        fields = ('username', 'email', 'birthdate', 'password1', 'password2')

        birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )