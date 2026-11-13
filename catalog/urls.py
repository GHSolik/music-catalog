from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("artists/", views.artist_list, name="artist_list"),
    path("artists/<int:pk>/", views.artist_detail, name="artist_detail"),

    path("albums/", views.album_list, name="album_list"),
    path("albums/<int:pk>/", views.album_detail, name="album_detail"),
]