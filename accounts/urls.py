from django.urls import path, include
from . import views

# Pour éviter les conflits si des vus ont les mêmes noms
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', accounts_views.login_user, name = 'login_user'),
    path('logout/', accounts_views.logout_user, name = 'logout_user'),
    path('signup/', accounts_views.signup_user, name = 'signup_user'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset-password-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #path('add/favourite/<slug:slug_thread_league>', views.add_favourite_competition, name='add_favourite_competition'),
    #path('remove/favourite/<slug:slug_thread_league>', views.remove_favourite_competition, name='remove_favourite_competition'),
]