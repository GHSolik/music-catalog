
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArtistForm, AlbumForm, TrackForm
from .models import Artist, Album, Track


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


@login_required
@permission_required("catalog.change_artist", raise_exception=True)
def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)

    if request.method == "POST":
        form = ArtistForm(
            request.POST,
            request.FILES,
            instance=artist
        )

        if form.is_valid():
            form.save()
            return redirect("artist_detail", pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)

    return render(
        request,
        "catalog/artist_form.html",
        {
            "form": form,
            "artist": artist,
            "is_edit": True,
        }
    )


@login_required
@permission_required("catalog.change_album", raise_exception=True)
def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        form = AlbumForm(
            request.POST,
            request.FILES,
            instance=album
        )

        if form.is_valid():
            form.save()
            return redirect("album_detail", pk=album.pk)
    else:
        form = AlbumForm(instance=album)

    return render(
        request,
        "catalog/album_form.html",
        {
            "form": form,
            "album": album,
            "is_edit": True,
        }
    )

@login_required
@permission_required("catalog.delete_artist", raise_exception=True)
def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)

    if request.method == "POST":
        artist.delete()
        return redirect("artist_list")

    return render(
        request,
        "catalog/confirm_delete.html",
        {
            "object": artist,
            "object_type": "исполнителя",
            "cancel_url": "artist_detail",
        }
    )

@login_required
@permission_required("catalog.delete_album", raise_exception=True)
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        return redirect("album_list")

    return render(
        request,
        "catalog/confirm_delete.html",
        {
            "object": album,
            "object_type": "альбом",
            "cancel_url": "album_detail",
        }
    )

@login_required
@permission_required("catalog.change_track", raise_exception=True)
def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk)
    album = track.album

    if request.method == "POST":
        form = TrackForm(
            request.POST,
            request.FILES,
            instance=track,
            album=album
        )

        if form.is_valid():
            form.save()
            return redirect("album_detail", pk=album.pk)
    else:
        form = TrackForm(instance=track, album=album)

    return render(
        request,
        "catalog/track_form.html",
        {
            "form": form,
            "album": album,
            "track": track,
            "is_edit": True,
        }
    )


@login_required
@permission_required("catalog.delete_track", raise_exception=True)
def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    album = track.album

    if request.method == "POST":
        track.delete()
        return redirect("album_detail", pk=album.pk)

    return render(
        request,
        "catalog/confirm_delete.html",
        {
            "object": track,
            "object_type": "трек",
            "cancel_url": "album_detail",
            "cancel_pk": album.pk,
        }
    )
