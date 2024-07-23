# Useful libraries
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import os

# Django authentification
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from accounts.form import CustomUserCreationForm

# Model import
from django.contrib.auth.models import User
from accounts.models import favourites
from fora.models import threads_categories_match


def login_user(request) :
    """
    View function to login a user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: 1 -> The user exists and information are corrects. So, redirection to the home page.
                      2 -> The information are incorrect and the same page is returned with a error message.
    """
    if request.method == 'POST' :
            username = request.POST["username"]
            password = request.POST["password"]

            # Check if the user exists
            user = authenticate(request, username = username, password = password)
            
            if user != None : 
                login(request, user)
                return redirect(os.environ.get('REDIRECTION'))
            else :
                messages.info(request, "Incorrect login or password !")

    form = AuthenticationForm()

    return render(request, "login.html", {'form': form})
    

def logout_user(request) :
    """
    View function to logout a user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response is a redirection to the home page.
    """
    logout(request)
    return redirect(os.environ.get('REDIRECTION'))


def signup_user(request) :
    """
    View function to sign up a user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The same page is returned with a error or success message.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # Check if the e-mail address is similar to one already registered
        email = request.POST.get('email')
        email_validate = User.objects.filter(email=email)

        if email_validate.exists() :
            # Add a custom error if the e-mail address is similar
            form.add_error('email', "A user with that email already exists.")

        else :
            if form.is_valid():
                username = form.cleaned_data['username']
        
                # Create a new user with the correct hashed password
                user = form.save() 
                messages.success(request, f"Account created for {username}!")    
                
           
        # Display validation errors in the form if the form is invalid
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)                 

    form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


def add_favourite_competition(request, slug_thread_league) :
    """
    View function to add a competition in the favourite of a user.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_league: Part of the url that indicates the league to add to favorites (challenge cup, top 14...).

    Returns:
        JsonResponse: 1. If the request method is 'POST' and the competition is successfully added to the user's favourites,
                         it returns a JSON response with details of the added competition.
                      2. If the request method is not 'POST' or the competition already exists in the user's favourites,
                         it returns a JSON response which is equal to none.
    """
    if request.method == 'POST':
        user = request.user
        
        verification = favourites.objects.filter(slug_competition=slug_thread_league, user=user)
        category = threads_categories_match.objects.get(slug_thread_league=slug_thread_league)

        if(not verification.exists()) :
            favourites.objects.create(name_competition=category.thread_league, user=user, slug_competition=slug_thread_league)
            
        context = {
            'slug_thread_category': category.slug_thread_category,
            'slug_thread_league': slug_thread_league,
            'thread_league': category.thread_league,
        }
        
        return JsonResponse(context)

    context = None
    return JsonResponse(context)


def remove_favourite_competition(request, slug_thread_league) :
    """
    View function to add a competition in the favourite of a user.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_league: Part of the url that indicates the league to add to favorites (challenge cup, top 14...).

    Returns:
        JsonResponse: 1. If the request method is 'POST' and the competition is successfully deleted to the user's favourites,
                         it returns a JSON response with with details of the deleted competition.
                      2. If the request method is not 'POST' or the competition already  doesn't exist in the user's favourites,
                         it returns a JSON response which is equal to none.
    """
    if request.method == 'POST':
        user = request.user

        verification = favourites.objects.filter(slug_competition=slug_thread_league, user=user)
        category = threads_categories_match.objects.get(slug_thread_league=slug_thread_league)

        if(verification.exists()) :
            verification.delete()

        context = {
            'slug_thread_league': slug_thread_league,
            'thread_league': category.thread_league,
            'slug_thread_category': category.slug_thread_category,
        }

        return JsonResponse(context)

    context = None
    return JsonResponse(context)

        
