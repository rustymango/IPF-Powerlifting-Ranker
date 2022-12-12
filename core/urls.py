from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PowerliftingView, rankDetail

urlpatterns = [
    path("stats/", PowerliftingView),
    path("stats/<int:pk>/", rankDetail),
]

# urlpatterns = format_suffix_patterns(urlpatterns)