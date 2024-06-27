from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.fora, name = 'fora'),
    path('categories/<slug:slug_thread_category>/<slug:slug_thread_league>/', views.categories, name = 'categories'),

    # Display a thread
    path('threads/<slug:slug_thread_category>/<slug:slug_thread_league>/<slug:slug_thread_comments>/', views.threads_, name = 'threads_'),

    # Display a tchat
    path('tchats/<slug:slug_tchat_category>/<slug:slug_tchat_name>/', views.tchats_, name='tchats_'),

    # Ne sert juste qu'à ajouter un commentaire sur un match
    path('add/comment/thread/<slug:slug_comment_category>/<slug:slug_thread_tchat>/', views.add_comment_thread, name='add_comment_thread'),
    path('add/comment/tchat/<slug:slug_tchat_name>/', views.add_comment_tchat, name='add_comment_tchat'),

    # Ne sert juste qu'à afficher les bons threads pour une catégorie
    path('display/threads/<slug:slug_category_thread>/', views.display_threads, name='display_threads'),

    # Ne sert juste qu'à afficher les bons tchats
    path('display/tchats/<slug:slug_tchat_name>/', views.display_tchats, name='display_tchats'),
]
