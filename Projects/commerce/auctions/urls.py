from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("watchlist/<int:item_id>", views.watchlist, name="watchlist"),
    path("account/<str:user>", views.user, name="user"),
    path("end/<int:item_id>", views.end, name="end")
]
