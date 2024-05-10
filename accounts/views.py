from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.form import CustomUserCreationForm

from django.contrib.auth.models import User

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView

def login_user(request) :
    if request.method == 'POST' :
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username = username, password = password)
            
            if user != None : 
                login(request, user)
                return redirect("http://127.0.0.1:8000/")
            else :
                messages.info(request, "Incorrect login or password !")

    form = AuthenticationForm()

    return render(request, "login.html", {'form': form})
    

def logout_user(request) :
    logout(request)
    return redirect("http://127.0.0.1:8000/")

def signup_user(request) :
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # Vérifier si l'adresse e-mail est similaire à une autre déjà enregistrée
        email = request.POST.get('email')
        email_validate = User.objects.filter(email=email)

        if email_validate.exists() :
            # Ajouter une erreur personnalisée si l'adresse e-mail est similaire
            form.add_error('email', "A user with that email already exists.")

        else :
            if form.is_valid():
                username = form.cleaned_data['username']
        
                # Créer un nouvel utilisateur avec le mot de passe haché correctement
                user = form.save() 
                messages.success(request, f"Account created for {username}!")    
                
           
        # Afficher les erreurs de validation dans le formulaire si le formulaire n'est pas valide
        for errors in form.errors.values():
            print(errors)
            for error in errors:
                messages.error(request, error)                 

    form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})