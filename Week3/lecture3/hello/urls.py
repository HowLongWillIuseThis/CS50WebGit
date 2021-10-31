from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("han/", views.han, name="han"),
    path("<str:name>", views.greet, name="greet"),
]