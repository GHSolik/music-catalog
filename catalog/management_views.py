
from .audio_metadata import read_audio_metadata
from .temp_audio import (
    save_temp_audio,
    get_temp_audio_path,
    open_temp_audio,
    delete_temp_audio,
)

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

    temp_token = None
    metadata_message = None
    temp_filename = None

    if request.method == "POST":
        action = request.POST.get("action", "save")
        temp_token = request.POST.get("temp_token", "")

        if action == "read_metadata":
            uploaded_file = request.FILES.get("audio_file")

            if uploaded_file:
                temp_token = save_temp_audio(
                    uploaded_file,
                    request.user
                )

                request.session[f"temp_audio_{temp_token}"] = uploaded_file.name
                temp_filename = uploaded_file.name

                path = get_temp_audio_path(
                    temp_token,
                    request.user
                )

                try:
                    metadata = read_audio_metadata(path)

                    data = request.POST.copy()

                    for field in [
                        "title",
                        "track_number",
                        "duration",
                    ]:
                        if metadata[field] is not None:
                            data[field] = metadata[field]

                    form = TrackForm(
                        data,
                        album=album
                    )

                    metadata_message = (
                        "Метаданные прочитаны. "
                        "Проверьте поля перед сохранением."
                    )

                except Exception:
                    form = TrackForm(
                        request.POST,
                        album=album
                    )

                    metadata_message = (
                        "Не удалось прочитать метаданные. "
                        "Заполните поля вручную."
                    )

            
            else:
                form = TrackForm(
                    initial={
                        "title": request.POST.get("title", ""),
                        "track_number": request.POST.get("track_number", ""),
                        "duration": request.POST.get("duration", ""),
                    },
                    album=album
                )

                metadata_message = (
                    "Сначала выберите аудиофайл."
                )


        else:
            uploaded_file = request.FILES.get("audio_file")

            if uploaded_file:
                temp_token = ""

            if not uploaded_file and temp_token:
                uploaded_file = open_temp_audio(
                    temp_token,
                    request.user
                )

            files = request.FILES.copy()

            if uploaded_file:
                files["audio_file"] = uploaded_file

            
            form = TrackForm(
                request.POST,
                files,
                album=album
            )

            try:
                if form.is_valid():
                    track = form.save(commit=False)
                    track.album = album
                    track.save()

                    if temp_token:
                        delete_after_save = True
                    else:
                        delete_after_save = False

                    saved = True
                else:
                    saved = False
            finally:
                if uploaded_file and temp_token:
                    uploaded_file.close()

            
            if saved:
                if delete_after_save:
                    delete_temp_audio(
                        temp_token,
                        request.user
                    )

                    request.session.pop(
                        f"temp_audio_{temp_token}",
                        None
                    )

                return redirect(
                    "album_detail",
                    pk=album.pk
                )




    else:
        form = TrackForm(album=album)

    
    if temp_token:
        path = get_temp_audio_path(
            temp_token,
            request.user
        )

        if path is not None:
            temp_filename = request.session.get(
                f"temp_audio_{temp_token}"
            )
        else:
            temp_token = None
            temp_filename = None


    return render(
        request,
        "catalog/track_form.html",
        {
            "form": form,
            "album": album,
            "temp_token": temp_token,
            "metadata_message": metadata_message,
            "temp_filename": temp_filename,
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
