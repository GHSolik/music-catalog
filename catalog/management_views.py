
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArtistForm, AlbumForm, TrackForm
from .models import Album


@login_required
def artist_add(request):
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)

        if form.is_valid():
            artist = form.save(commit=False)
            artist.created_by = request.user
            artist.save()

            return redirect("artist_list")
    else:
        form = ArtistForm()

    return render(
        request,
        "catalog/artist_form.html",
        {"form": form}
    )


@login_required
def album_add(request):
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)

        if form.is_valid():
            album = form.save(commit=False)
            album.created_by = request.user
            album.save()

            return redirect("album_list")
    else:
        form = AlbumForm()

    return render(
        request,
        "catalog/album_form.html",
        {"form": form}
    )



@login_required
def track_add(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    if request.method == "POST":
        form = TrackForm(
            request.POST,
            request.FILES,
            album=album
        )

        if form.is_valid():
            track = form.save(commit=False)
            track.album = album
            track.save()

            return redirect("album_detail", pk=album.pk)
    else:
        form = TrackForm(album=album)

    return render(
        request,
        "catalog/track_form.html",
        {
            "form": form,
            "album": album,
        }
    )
