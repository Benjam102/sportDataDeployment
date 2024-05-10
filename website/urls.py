from django.urls import path, include
from . import views

# On relie les URLs aux fonctions de views.py #
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('leagues/', views.leagues, name='leagues'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.matches, name='matches'),
    path('players/', views.players, name='players'),
    path('contact-us/', views.contact, name='contact'),
    path('image-sources/', views.imgSources, name='imgSources'),
    path('url-sources/', views.urlSources, name='urlSources'),
    path('match/<slug_match>/', views.presentationMatch, name='presentationMatch'),
]