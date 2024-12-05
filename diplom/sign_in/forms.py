from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser 
        fields = ('username', 'email', 'password1', 'password2')



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser .objects.filter(email=email).exists():
            raise forms.ValidationError("Электронная почта уже зарегистрирована.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")