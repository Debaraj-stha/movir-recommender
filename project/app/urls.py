from django.urls import path
from .views import *
urlpatterns=[
    path('',load_index)
]