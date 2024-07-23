from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

# Importation des modèles
from .models import matches, teams, odds, rankings, players, sources, compositions

# Importation des fonctions de scraping
from fora.models import threads_categories_match, threads_match, threads_comments_match
from prediction.models import predictions_matches
from accounts.models import favourites

# Utile
from django.db.models import Max
from django.forms.models import model_to_dict
from django.db.models import Q
from .utils import form_match, associate_weather_code, user_prediction
from django.http import JsonResponse
import json
from django.core import serializers
from django.db.models import Count
from django.utils.functional import SimpleLazyObject

# Page d'acceuil
def homePage(request) :
    
    if request.user.is_authenticated:
        try:
            user = request.user
            user_prediction = predictions_matches.objects.filter(user_prediction=user)
            
        except predictions_matches.DoesNotExist:
            user_prediction = None
       
        context = {
            'user_prediction': user_prediction,
        }
 
    else :

        context = {
            'user_prediction': None,
        }

    return render(request, "homePage.html", context)


def fixtures(request) :    
    # Récupérer tous les noms des catégories sans doublon, triés par ordre alphabétique
    categories = threads_categories_match.objects.values_list('thread_category', flat=True).distinct() 
   
    # Créer un dictionnaire pour stocker les leagues par catégories
    leagues_by_categories = {}

    # Lier chaque league à une catégorie
    for category in categories:
        categories = threads_categories_match.objects.filter(thread_category=category).order_by('thread_league')

        if (category != 'Favourites') :
            leagues_by_categories[category] = categories
        else :
            leagues_by_categories[category] = []

    # Favoris
    compe_fav = []
    if request.user.is_authenticated:
        user = request.user
        competitions_favourites = favourites.objects.filter(user=user)

        for c in competitions_favourites :   
            dico = {                                            # mettre les memes nom que pour les objets threads_category
                'slug_thread_league': c.slug_competition,
                'slug_thread_category': threads_categories_match.objects.get(slug_thread_league=c.slug_competition).slug_thread_category,
                'thread_league': c.name_competition
            }
            leagues_by_categories['Favourites'].append(dico)
            compe_fav.append(c.name_competition)
        

    # Passer les matchs récupérés au contexte du template
    context = {
        'compe_fav': compe_fav,
        'leagues_by_categories': leagues_by_categories
    }

    return render(request, "fixtures.html", context)


def display_matches(request, slug_category_thread) :
    """
    View function to display matches when a competition is checked.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_category_thread: Part of the url that indicates the competition checked.

    Returns:
        JsonResponse: 1. If the request method is 'GET', we find matches based on the competition checked and
                         it returns a JSON response with details on the standings.
                      2. If the request method is not 'GET', it returns a JSON response which is equal to none.
    """
    if request.method == 'GET':
        # Recovery of the competiton name
        category_selected = threads_categories_match.objects.get(slug_thread_league=slug_category_thread).thread_league
        
        if(category_selected != 'Closest') :
            upcoming_matches = matches.objects.filter(status='Scheduled', competition=category_selected).exclude(date__isnull=True).exclude(kickoff__isnull=True)
            upcoming_matches = upcoming_matches.order_by('date', 'kickoff').values()
        else :
            upcoming_matches = matches.objects.filter(status='Scheduled').exclude(date__isnull=True).exclude(kickoff__isnull=True)
            upcoming_matches = upcoming_matches.order_by('date', 'kickoff')[:10].values() # Just the first 10

        upcoming_matches_list = []

        # Creating a dictionary to transmit data via json
        for m in upcoming_matches :
            
            try :
                logo_home_team = teams.objects.get(name=m['home_team_id']).logo
            except teams.DoesNotExist :
                logo_home_team = None

            try :
                logo_away_team = teams.objects.get(name=m['away_team_id']).logo
            except teams.DoesNotExist :
                logo_away_team = None

            d = {
                'key_id': m['key_id'],
                'date': m['date'],
                'kickoff': m['kickoff'],
                'home_team': m['home_team_id'], 
                'logo_home_team': logo_home_team,
                'away_team': m['away_team_id'],  
                'logo_away_team': logo_away_team,
                'competition': m['competition'],
            }

            upcoming_matches_list.append(d)

        # Case where there is no match
        if len(upcoming_matches_list) == 0 :
            upcoming_matches_list = None

        today_date = datetime.now().date()
        tomorrow_date = today_date + timedelta(days=1)

        context = {
            'upcoming_matches_list': upcoming_matches_list,
            'today_date' : today_date,
            'tomorrow_date' : tomorrow_date,
        }

    else :
        context = None

    return JsonResponse(context)


#locale: 0 si c'est le classement général, -1 si c'est juste a l'exterieur et 1 a domicile
def presentationMatch(request, slug_match) :
    match = matches.objects.get(key_id=slug_match)

    # Prediction
    try :
        user = request.user
        if not user.is_authenticated:
            # Utilisateur non authentifié, utilisez une valeur par défaut pour user_id
            user_id = -1
            prediction = predictions_matches.objects.get(prediction_match=match, user_prediction=user_id)
        else:
            # Utilisateur authentifié
            prediction = predictions_matches.objects.get(prediction_match=match, user_prediction=user)
    
    except predictions_matches.DoesNotExist :
        prediction = None

    home_prediction1 = None
    away_prediction1 = None 
    home_prediction2 = None 
    away_prediction2 = None

    if prediction != None :
        home_prediction1, away_prediction1, home_prediction2, away_prediction2 = user_prediction(prediction)

    # Preview
    try :
        # Trouver le thread associé au match
        threads_ = threads_match.objects.get(key_id=match)

        # Compter le nombre total de commentaires pour ce thread
        comment_count = threads_comments_match.objects.filter(thread=threads_).count()

        # Récupérer la date du commentaire le plus récent pour ce thread
        comments = threads_comments_match.objects.filter(thread=threads_)
        latest_comment_date = comments.aggregate(latest_comment=Max('date'))["latest_comment"]
        
        if latest_comment_date != None :
            latest_comment = threads_comments_match.objects.get(thread=threads_, date=latest_comment_date)
        else :
            latest_comment = None  
    
    except threads_match.DoesNotExist as e: # Pour les anciens matches
            # print(f"Thread for match with key_id {slug_match} do not exist: {e}")
            comment_count = 0
            latest_comment = None
    
    try:
        match_slug_league_category = threads_categories_match.objects.get(thread_league=match.competition)
        slug_thread_category = match_slug_league_category.slug_thread_category
        slug_thread_league = match_slug_league_category.slug_thread_league
    except threads_categories_match.DoesNotExist :
        match_slug_league_category = None
        slug_thread_category = None
        slug_thread_league = None
        
    # Form for the current home team over 5 last matches (in relation to the current match)
    last_matches_home_team = matches.objects.filter((Q(home_team=match.home_team) | Q(away_team=match.home_team)) & Q(date__lt=match.date)).order_by('-date') # __lt (less than) == <
    form_home_team = last_matches_home_team[:5] 
  
    # Form for the current away team over 5 last matches (in relation to the current match)
    last_matches_away_team = matches.objects.filter((Q(home_team=match.away_team) | Q(away_team=match.away_team)) & Q(date__lt=match.date)).order_by('-date')
    form_away_team = last_matches_away_team[:5]

    try :
        rank_home_team = rankings.objects.get(competition=match.competition, team=match.home_team, year=match.date.year, locale=0).rank
        rank_away_team = rankings.objects.get(competition=match.competition, team=match.away_team, year=match.date.year, locale=0).rank
    except :
        rank_home_team = None
        rank_away_team = None

    # Odds
    try:
        match_odds = odds.objects.get(key_id=slug_match)
    except odds.DoesNotExist as e:
        # Gestion du cas où aucun objet n'est trouvé
        #print(f"Odds for match with key_id {slug_match} do not exist: {e}")
        match_odds = None
    
    # Meteo
    general_weather = associate_weather_code(match.weather_code)
    
    # Line up
    try:
        match_composition_home = compositions.objects.get(key_id=slug_match, local_team=1)
        match_composition_away = compositions.objects.get(key_id=slug_match, local_team=0)
    except compositions.DoesNotExist as e:
        # Gestion du cas où aucun objet n'est trouvé
        #print(f"Compositions for match with key_id {slug_match} do not exist: {e}")
        match_composition_home = None
        match_composition_away = None

    # H2H
    h2h = matches.objects.filter(((Q(home_team=match.home_team) & Q(away_team=match.away_team)) | (Q(home_team=match.away_team) & Q(away_team=match.home_team))) & Q(date__lt=match.date)).order_by('-date')
    h2h_home_away_team = matches.objects.filter(Q(home_team=match.home_team) & Q(away_team=match.away_team) & Q(date__lt=match.date)).order_by('-date')

    # Standings
    competitions = rankings.objects.filter(year=match.date.year, team=match.home_team).values_list('competition', flat=True).distinct()
    standings = rankings.objects.filter(year=match.date.year, competition=match.competition, locale=0).order_by('rank') # celle du match
    nb_teams_pool = 0
    nb_pools = 0
    pools_teams = None
    
    if standings.exists() :
        if standings[0].pool != None :
            standings = standings.order_by('pool')
            nb_teams_pool = standings.filter(pool='1').count() #standings.values('pool').annotate(equipes_count=Count('pool'))
            nb_pools = standings.filter(competition=match.competition).values('pool').distinct().count()

            pools_teams = {}
            for standing in standings:
                pool = standing.pool
                if pool not in pools_teams :
                    pools_teams[pool] = []

                pools_teams[pool].append(standing)

    # Home team
    standings_home = rankings.objects.filter(year=match.date.year, competition=match.competition, locale=1).order_by('rank') # celle du match
    
    # Away team
    standings_away = rankings.objects.filter(year=match.date.year, competition=match.competition, locale=-1).order_by('rank') # celle du match

    # Draw
    try :
        final_match = matches.objects.get(date__year=match.date.year, competition=match.competition, phase='Finale')
    except matches.DoesNotExist :
        final_match = None
    
    semi_final_match = matches.objects.filter(date__year=match.date.year, competition=match.competition, phase='1/2 finale')
    
    if (len(semi_final_match) == 0) :
        semi_final_match = None

    quarter_final_match = matches.objects.filter(date__year=match.date.year, competition=match.competition, phase='1/4 finale')
    
    if (len(quarter_final_match) == 0) :
        quarter_final_match = None
    
    round_of_16_match = matches.objects.filter(date__year=match.date.year, competition=match.competition, phase='8ème de finale')
    
    if (len(round_of_16_match) == 0) :
        round_of_16_match = None

    context = {
        'match': match,
        'prediction': prediction,
        'home_prediction1': home_prediction1,
        'away_prediction1': away_prediction1,
        'home_prediction2': home_prediction2,
        'away_prediction2': away_prediction2,
        'slug_thread_category': slug_thread_category,
        'slug_thread_league': slug_thread_league,
        'comment_count': comment_count,
        'latest_comment': latest_comment,
        'form_home_team': form_match(form_home_team, match.home_team.name),
        'form_away_team': form_match(form_away_team, match.away_team.name),
        'rank_home_team': rank_home_team,
        'rank_away_team' : rank_away_team,
        'match_odds': match_odds,
        'general_weather': general_weather,
        'match_composition_home': match_composition_home,
        'match_composition_away': match_composition_away,
        'last_matches_home_team': form_match(last_matches_home_team, match.home_team.name),
        'last_matches_away_team': form_match(last_matches_away_team, match.away_team.name),
        'h2h_home_team': form_match(h2h_home_away_team, match.home_team.name),
        'h2h_away_team': form_match(h2h_home_away_team, match.away_team.name),
        'competitions': competitions,
        'standings': standings,
        'nb_teams_pool': nb_teams_pool,
        'nb_pools': range(1, nb_pools + 1),
        'pools_teams': pools_teams,
        'standings_home': standings_home,
        'standings_away': standings_away,
        'final_match': final_match,
        'semi_final_match': semi_final_match,
        'quarter_final_match': quarter_final_match,
        'round_of_16_match': round_of_16_match,
    }

    return render(request, "match/match.html", context)


def get_standings(request, slug_match, year_competiton) :
    """
    View function to have information on standings.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_match: Part of the url that indicates the match where we want to have access to the ranking.
        year_competiton: Part of the url that indicates the year and the competition of the match.

    Returns:
        JsonResponse: 1. If the request method is 'GET' and standings are successfully found,
                         it returns a JSON response with details on the standings.
                      2. If the request method is not 'GET', it returns a JSON response which is equal to none.
    """

    if request.method == 'GET':
        # Data separation
        year = year_competiton[0:4]            
        competiton = year_competiton[4:]

        # Match and ranking recovery
        match = matches.objects.get(key_id = slug_match)
        standings = rankings.objects.filter(year=year, competition=competiton, locale=0).order_by('rank')

        nb_teams_pool = 0
        nb_pools = 0
        pools_teams = None

        ranks_list = []
        
        if standings.exists() :
            if standings[0].pool != None :
                standings = standings.order_by('pool')
                nb_teams_pool = standings.filter(pool='1').count() 
                nb_pools = standings.filter(competition=match.competition).values('pool').distinct().count()

                pools_teams = {}
                ranks_list = list(standings.values())
                
                for k in range(0, len(standings)) :
                    pool = standings[k].pool

                    if pool not in pools_teams :
                        pools_teams[pool] = []

                    try:
                        ranks_list[k]['logo'] = standings[k].team.logo
                    except teams.DoesNotExist:
                        ranks_list[k]['logo'] = None

                    # Team ranking by pool
                    pools_teams[pool].append(ranks_list[k])

            else :
                ranks_list = list(standings.values())
                for k in range(0, len(standings)) :
                    try:
                        ranks_list[k]['logo'] = standings[k].team.logo
                    except teams.DoesNotExist:
                        ranks_list[k]['logo'] = None

        context = {
            'ranks_list': ranks_list,
            'nb_teams_pool': int(nb_teams_pool),
            'nb_pools': list(range(1, nb_pools + 1)),
            'pools_teams': pools_teams,
        }

    else :
        context = None

    # JSON data in HTTP response
    return JsonResponse(context, safe=False)


def player(request, slug_match, player_id) :
    """
    View function to have information on a player.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_match: Part of the url that indicates the match where we find the player.
        player_id: Part of the url that indicates the player we want information on.

    Returns:
        HttpResponse: The HTTP response containing the rendered player page with information on it.
    """

    try :
        player_info = players.objects.get(player_id=player_id)
    except players.DoesNotExist :
        player_info = None
        
    try :
        player_club_logo = teams.objects.get(name=player_info.club).logo
    except teams.DoesNotExist :
        player_club_logo = None

    context = {
        'player_info': player_info,
        'player_club_logo': player_club_logo,
    }

    return render(request, "player.html", context)


def team(request, slug_match, team_id) :
    """
    View function to have information on a team.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_match: Part of the url that indicates the match where we find the team.
        player_id: Part of the url that indicates the team we want information on.

    Returns:
        HttpResponse: The HTTP response containing the rendered team page with information on it.
    """

    try :
        team_info = teams.objects.get(name=team_id)
    except players.DoesNotExist :
        team_info = None

    context = {
        'team_info': team_info,
    }

    return render(request, "team.html", context)


def imgSources(request) :
    """
    View function to have information on image sources.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered source page.
    """
    
    img_sources = sources.objects.all()

    context = {
        'img_sources': img_sources,
    }
    
    return render(request, "imgSources.html", context=context) 


# Not implemented
def old_standings(request) :
    """
    View function to have information on old standings (Backend not implemented).

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered standing page with information on all old standings.
    """
    return render(request, "standings.html")


  
  
