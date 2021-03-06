from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit", views.edit, name="edit"),
    path("wiki/<str:title>/change", views.change, name="change")
]
