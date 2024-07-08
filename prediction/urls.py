from django.urls import path, include
from . import views


urlpatterns = [
    path('<slug:slug_match>', views.predictionMatch, name = 'predictionMatch'),
]