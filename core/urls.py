from django.contrib import admin
from django.urls import path
from .views import display_rank

urlpatterns = [
    path('', display_rank),
    path("admin/", admin.site.urls)
]
