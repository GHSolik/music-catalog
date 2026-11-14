
from django.shortcuts import render, get_object_or_404

from .models import Artist, Album


def home(request):
    return render(request, "catalog/home.html")


def artist_list(request):
    artists = Artist.objects.all().order_by("name")

    return render(request, "catalog/artist_list.html", {
        "artists": artists,
    })


def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    albums = artist.albums.all().order_by("release_date", "title")

    return render(request, "catalog/artist_detail.html", {
        "artist": artist,
        "albums": albums,
    })


def album_list(request):
    albums = Album.objects.select_related("artist").order_by(
        "artist__name", "title"
    )

    return render(request, "catalog/album_list.html", {
        "albums": albums,
    })


def album_detail(request, pk):
    album = get_object_or_404(
        Album.objects.select_related("artist").prefetch_related("tracks"),
        pk=pk
    )

    return render(request, "catalog/album_detail.html", {
        "album": album,
        "tracks": album.tracks.all(),
    })
