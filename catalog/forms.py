
from django import forms

from .models import Artist, Album, Track


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name", "description", "image"]

        labels = {
            "name": "Название исполнителя",
            "description": "Описание",
            "image": "Изображение исполнителя",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Введите название исполнителя"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Введите описание исполнителя"}
            ),
        }


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

        labels = {
            "title": "Название альбома",
            "artist": "Исполнитель",
            "release_date": "Дата выхода",
            "genre": "Жанр",
            "description": "Описание",
            "cover": "Обложка альбома",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Введите название альбома"}
            ),
            "release_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Введите описание альбома"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["artist"].empty_label = "Выберите исполнителя"


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = [
            "title",
            "track_number",
            "duration",
            "audio_file",
        ]

        labels = {
            "title": "Название композиции",
            "track_number": "Номер композиции",
            "duration": "Длительность",
            "audio_file": "Аудиофайл",
        }

        
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Введите название композиции"
                }
            ),
            "track_number": forms.NumberInput(
                attrs={"min": 1}
            ),
            "audio_file": forms.FileInput(
                attrs={"accept": ".mp3,audio/mpeg"}
            ),
        }


        help_texts = {
            "duration": "Укажите длительность в формате ЧЧ:ММ:СС.",
        }

    def __init__(self, *args, album=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.album = album

    def clean_track_number(self):
        number = self.cleaned_data["track_number"]

        if self.album is not None:
            exists = Track.objects.filter(
                album=self.album,
                track_number=number
            )

            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)

            if exists.exists():
                raise forms.ValidationError(
                    "Трек с таким номером уже существует "
                    "в этом альбоме."
                )

        return number
