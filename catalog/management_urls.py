
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
]
