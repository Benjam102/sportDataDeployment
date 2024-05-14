from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.fora, name = 'fora'),
    path('<slug_type>/<slug_category>/', views.categories, name = 'categories'),
    path('<slug_type>/<slug_category>/<slug_thread>/', views.threads_, name = 'threads_'),
    # Ne sert juste qu'à ajouter un commentaire sur un match
    path('add_comment/<slug_category>/<slug_thread>/', views.add_comment, name='add_comment'),
    # Ne sert juste qu'à afficher les bons threads pour une catégorie
    path('<slug_category>/', views.display_category, name='display_category')
]
