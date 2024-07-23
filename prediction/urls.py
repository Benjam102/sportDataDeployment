from django.urls import path, include
from . import views


urlpatterns = [
    path('<slug:slug_match>', views.prediction_match, name = 'prediction_match'),
]