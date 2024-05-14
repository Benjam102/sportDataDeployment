from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

# Importation des modèles
from .models import up_match
from fora.views import threads_

# Importation des fonctions de scraping
from website.scraping.upcoming_matches import get_upcoming_matches
from website.scraping.referee import get_referee
from website.scraping.meteo import get_weather
from fora.models import tchat_match_comment, tchat_match_category, threads

# Utile
from django.db.models import Max

# Page d'acceuil #
def homePage(request) :

    #get_upcoming_matches("https://www.rugbypass.com/fixtures/")

    #get_referee('https://rugbyreferee.net/category/appointments/') 

    # Récupérer les 4 matchs les plus proches ordonnés par date puis par heure
    upcoming_matches = up_match.objects.all().order_by('date', 'hour')[:4]

    today_date = datetime.now().date()
    tomorrow_date = today_date + timedelta(days=1)

    # Récupérer les compétitions distinctes associées aux matchs et les trier par ordre alphabétique
    # Renvoie un tuple -> {'league': 'nom'} (dictionnaire)
    competitions_sorted = up_match.objects.values('league').distinct().order_by('league')

    # Récupérer tous les noms des catégories sans doublon, triés par ordre alphabétique
    categories = tchat_match_category.objects.values_list('country', flat=True).order_by('country').distinct()

    # Créer un dictionnaire pour stocker les leagues par catégories
    leagues_by_categories = {}

    # Lier chaque league à une catégorie
    for category in categories:
        categories = tchat_match_category.objects.filter(country=category).order_by('title')
        leagues_by_categories[category] = categories

    # Passer les matchs récupérés au contexte du template
    context = {
        'upcoming_matches': upcoming_matches,
        'num_matches': len(upcoming_matches),  # Nombre de matchs récupérés
        'today_date' : today_date,
        'tomorrow_date' : tomorrow_date,
        'competitions_sorted' : competitions_sorted,
        'categories_by_country': leagues_by_categories
    }

    return render(request, "homePage.html", context)

def presentationMatch(request, slug_match) :
    match_ = up_match.objects.get(slug=slug_match)
    threads_ = threads.objects.get(match=match_)

    # Compter le nombre total de commentaires pour ce thread
    comment_count = tchat_match_comment.objects.filter(thread=threads_).count()

    # Récupérer la date du commentaire le plus récent pour ce thread
    comments = tchat_match_comment.objects.filter(thread=threads_)
    latest_comment_date = comments.aggregate(latest_comment=Max('date'))["latest_comment"]
    
    if latest_comment_date != None :
        latest_comment = tchat_match_comment.objects.get(thread=threads_, date=latest_comment_date)
    else :
        latest_comment = None  
      
    category_slug = tchat_match_category.objects.get(title=match_.league).slug_title
    country_slug = tchat_match_category.objects.get(title=match_.league).slug_country

    context = {
        "match_": match_,
        "category_slug": category_slug,
        "comment_count": comment_count,
        "latest_comment": latest_comment,
        "country_slug": country_slug,
    }

    return render(request, "match.html", context)


def leagues(request) :

    return render(request, "standings.html")

def teams(request) :

    return render(request, "teams.html")

def matches(request) :

    return render(request, "matches.html")

def players(request) :

    return render(request, "players.html")
         
def contact(request) :

    return render(request, "contact.html")  

def imgSources(request) :

    return render(request, "imgSources.html")   

def urlSources(request) :

    return render(request, "urlSources.html")   
