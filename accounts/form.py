from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Permet d'ajouter le champs email lors de l'inscription
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')