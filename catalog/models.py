
from django.conf import settings
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="artists/",
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums"
    )
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.artist.name} — {self.title}"


class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="tracks"
    )
    title = models.CharField(max_length=200)
    track_number = models.PositiveIntegerField()
    duration = models.DurationField(null=True, blank=True)
    audio_file = models.FileField(
        upload_to="tracks/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["track_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "track_number"],
                name="unique_album_track_number"
            )
        ]

    def __str__(self):
        return f"{self.track_number}. {self.title}"
