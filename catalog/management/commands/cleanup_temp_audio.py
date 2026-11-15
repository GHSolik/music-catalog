
import time

from django.core.management.base import BaseCommand

from catalog.temp_audio import TEMP_AUDIO_ROOT


class Command(BaseCommand):
    help = "Удаляет временные аудиофайлы старше 24 часов."

    def handle(self, *args, **options):
        if not TEMP_AUDIO_ROOT.exists():
            self.stdout.write(
                "Папка временных файлов отсутствует."
            )
            return

        now = time.time()
        max_age = 24 * 60 * 60
        deleted = 0

        for user_folder in TEMP_AUDIO_ROOT.iterdir():
            if not user_folder.is_dir():
                continue

            for file_path in user_folder.iterdir():
                if not file_path.is_file():
                    continue

                try:
                    age = now - file_path.stat().st_mtime

                    if age > max_age:
                        file_path.unlink()
                        deleted += 1

                except OSError as error:
                    self.stderr.write(
                        f"Не удалось удалить {file_path.name}: {error}"
                    )

            try:
                if not any(user_folder.iterdir()):
                    user_folder.rmdir()
            except OSError:
                pass

        self.stdout.write(
            self.style.SUCCESS(
                f"Очистка завершена. Удалено файлов: {deleted}"
            )
        )
