
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("artists/", views.artist_list, name="artist_list"),
    path("albums/random/", views.random_album, name="random_album"),
    path("artists/<int:pk>/", views.artist_detail, name="artist_detail"),

    path("albums/", views.album_list, name="album_list"),
    path("albums/<int:pk>/", views.album_detail, name="album_detail"),
    path("albums/<int:pk>/rate/", views.rate_album, name="rate_album"),

    path("search/", views.search, name="search"),
    path("", include("catalog.management_urls")),
]
