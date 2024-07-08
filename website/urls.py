from django.urls import path, include
from . import views

# On relie les URLs aux fonctions de views.py #
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('standings/', views.standings, name='standings'),
    path('teams/', views.teams_, name='teams_'),
    path('matches/', views.matches, name='matches'),
    path('image-sources/', views.imgSources, name='imgSources'),
    path('match/<slug:slug_match>/', views.presentationMatch, name='presentationMatch'),
    path('match/<slug:slug_match>/player/<str:player_id>/', views.player, name='player'),
    path('match/<slug:slug_match>/<str:year_competiton>/', views.get_standings, name='get_standings'),

    # Ne sert juste qu'à afficher les bons threads pour une catégorie
    path('display/matches/<slug:slug_category_thread>/', views.display_matches, name='display_matches'),
]