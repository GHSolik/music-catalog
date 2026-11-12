# Music Catalog

Учебный проект на Django — музыкальная энциклопедия с каталогом исполнителей, альбомов и композиций.

## Технологии

- Python
- Django
- SQLite
- HTML, CSS, Django Templates
- Git и GitHub

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd music_catalog
```

### 2. Создание виртуального окружения

```bash
py -m venv .venv
```

Активация в Windows (Command Prompt):

```cmd
.venv\Scripts\activate.bat
```

### 3. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py migrate
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

После запуска приложение доступно по адресу:

http://127.0.0.1:8000/

Административная панель:

http://127.0.0.1:8000/admin/

Для создания администратора:

```bash
python manage.py createsuperuser
```

## Структура проекта

- `config/` — настройки Django.
- `catalog/` — модели исполнителей, альбомов и треков.
- `accounts/` — функциональность пользователей.
- `templates/` — HTML-шаблоны.
- `static/` — CSS, JavaScript и статические ресурсы.
- `media/` — загружаемые изображения и аудиофайлы.

## Командная разработка

Разработка ведётся в отдельных Git-ветках. Готовые изменения объединяются с `main` через Pull Requests.

## Статус

Проект находится в разработке.