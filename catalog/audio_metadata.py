
from datetime import timedelta

from mutagen import File
from mutagen.id3 import ID3, ID3NoHeaderError


def read_audio_metadata(file_path):
    result = {
        "title": None,
        "track_number": None,
        "duration": None,
    }

    audio = File(file_path)

    if audio is None:
        raise ValueError("Не удалось распознать аудиофайл.")

    if audio.info is not None:
        seconds = round(audio.info.length)
        result["duration"] = str(
            timedelta(seconds=seconds)
        )

    try:
        tags = ID3(file_path)
    except ID3NoHeaderError:
        return result

    title = tags.get("TIT2")
    if title:
        result["title"] = str(title)

    track_number = tags.get("TRCK")
    if track_number:
        number = str(track_number).split("/")[0]

        if number.isdigit() and int(number) > 0:
            result["track_number"] = int(number)

    return result
