FROM python:3.12-slim-bookworm

# Установка UV для управления зависимостями
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Создание рабочей директории
WORKDIR /app

# Копирование проекта в контейнер
ADD . /app


# Установка зависимостей из lock-файла
RUN uv sync --frozen --no-group dev

ENV PATH="/app/.venv/bin:$PATH"

# Выполнение миграций при запуске контейнера
CMD alembic upgrade head && fastapi dev main.py --host 0.0.0.0 --port 8000
