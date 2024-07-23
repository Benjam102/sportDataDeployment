from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.fora, name = 'fora'),
    path('categories/<slug:slug_thread_category>/<slug:slug_thread_league>/', views.categories, name = 'categories'),

    # Display the discussion
    path('threads/<slug:slug_thread_category>/<slug:slug_thread_league>/<slug:slug_thread_comments>/', views.threads_, name = 'threads_'),
    path('tchats/<slug:slug_tchat_category>/<slug:slug_tchat_name>/', views.tchats_, name='tchats_'),

    # Add a comment
    path('add/comment/thread/<slug:slug_comment_category>/<slug:slug_thread_tchat>/', views.add_comment_thread, name='add_comment_thread'),
    path('add/comment/tchat/<slug:slug_tchat_name>/', views.add_comment_tchat, name='add_comment_tchat'),

    # Display with checkbooes
    path('display/threads/<slug:slug_category_thread>/', views.display_threads, name='display_threads'),
    path('display/tchats/<slug:slug_tchat_name>/', views.display_tchats, name='display_tchats'),
]
