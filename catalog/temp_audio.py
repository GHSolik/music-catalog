
from pathlib import Path
from uuid import UUID, uuid4

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage


TEMP_AUDIO_ROOT = Path(settings.BASE_DIR) / "temp_audio_uploads"

temp_storage = FileSystemStorage(
    location=TEMP_AUDIO_ROOT
)


def save_temp_audio(uploaded_file, user):
    token = uuid4().hex
    filename = f"{user.pk}/{token}"

    temp_storage.save(filename, uploaded_file)

    return token


def get_temp_audio_path(token, user):
    try:
        token = UUID(token).hex
    except (ValueError, AttributeError, TypeError):
        return None

    path = TEMP_AUDIO_ROOT / str(user.pk) / token

    if not path.is_file():
        return None

    return path


def open_temp_audio(token, user):
    path = get_temp_audio_path(token, user)

    if path is None:
        return None

    return File(
        path.open("rb"),
        name=f"{token}.mp3"
    )


def delete_temp_audio(token, user):
    path = get_temp_audio_path(token, user)

    if path is not None:
        path.unlink(missing_ok=True)
