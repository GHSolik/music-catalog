
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

    tracks = album.tracks.all()

    total_seconds = 0

    for track in tracks:
        if track.duration:
            total_seconds += int(track.duration.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        total_duration = f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        total_duration = f"{minutes}:{seconds:02d}"

    return render(request, "catalog/album_detail.html", {
        "album": album,
        "tracks": tracks,
        "total_duration": total_duration,
        "has_duration": any(track.duration is not None for track in tracks),
    })
