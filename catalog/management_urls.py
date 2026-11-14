
from django.urls import path

from . import management_views

urlpatterns = [
    path(
        "artists/add/",
        management_views.artist_add,
        name="artist_add"
    ),
    path(
        "albums/add/",
        management_views.album_add,
        name="album_add"
    ),
    path(
        "albums/<int:album_id>/tracks/add/",
        management_views.track_add,
        name="track_add"
    ),

    path(
        "artists/<int:pk>/edit/",
        management_views.artist_edit,
        name="artist_edit"
    ),
    path(
        "albums/<int:pk>/edit/",
        management_views.album_edit,
        name="album_edit"
    ),

    path(
        "artists/<int:pk>/delete/",
        management_views.artist_delete,
        name="artist_delete"
    ),
    path(
        "albums/<int:pk>/delete/",
        management_views.album_delete,
        name="album_delete"
    ),

]
