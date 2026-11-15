import hashlib

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q


from .models import Artist, Album


def home(request):
    latest_albums = (
        Album.objects
        .select_related("artist")
        .order_by("-pk")[:6]
    )

    featured_artists = (
        Artist.objects
        .order_by("-pk")[:6]
    )

    # Выбираем альбом дня
    album_of_the_day = None

    album_ids = list(
        Album.objects.order_by("pk").values_list("pk", flat=True)
    )

    if album_ids:
        today = timezone.localdate().isoformat()

        date_hash = hashlib.sha256(
            today.encode("utf-8")
        ).hexdigest()

        index = int(date_hash, 16) % len(album_ids)

        album_of_the_day = (
            Album.objects
            .select_related("artist")
            .get(pk=album_ids[index])
        )

    return render(request, "catalog/home.html", {
        "latest_albums": latest_albums,
        "featured_artists": featured_artists,
        "album_of_the_day": album_of_the_day,
    })


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

def search(request):
    query = request.GET.get("q", "").strip()

    artists = Artist.objects.none()
    albums = Album.objects.none()

    if query:
        artists = Artist.objects.filter(
            name__icontains=query
        ).order_by("name")

        albums = Album.objects.select_related("artist").filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        ).order_by("artist__name", "title")

    return render(request, "catalog/search.html", {
        "query": query,
        "artists": artists,
        "albums": albums,
    })

def random_album(request):
    album = Album.objects.order_by("?").first()

    if album is None:
        return redirect("album_list")

    return redirect("album_detail", pk=album.pk)