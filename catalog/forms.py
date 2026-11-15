
from django import forms

from .models import Artist, Album, Track


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name", "description", "image"]


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            "title",
            "artist",
            "release_date",
            "genre",
            "description",
            "cover",
        ]
        widgets = {
            "release_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            )
        }



class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = [
            "title",
            "track_number",
            "duration",
            "audio_file",
        ]

    def __init__(self, *args, album=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.album = album

    def clean_track_number(self):
        number = self.cleaned_data["track_number"]

        if self.album is not None:
            exists = Track.objects.filter(
                album=self.album,
                track_number=number
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "Трек с таким номером уже существует "
                    "в этом альбоме."
                )

        return number
