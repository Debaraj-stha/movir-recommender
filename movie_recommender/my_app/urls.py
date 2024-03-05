from django.urls import path
from .views import *
urlpatterns = [
    path('',loadIndex,name="index"),
    path('get_recommendation',getRecommendations),
    path('search',get_search_movie)
]
