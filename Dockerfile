# Використовуємо офіційний легкий образ Python
FROM python:3.11.3-slim-bullseye

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо Python-пакети без кешу
RUN python -m pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . /app

# Не буферизуємо вивід Python (для миттєвих логів)
ENV PYTHONUNBUFFERED=1

# Відкриваємо порт
EXPOSE 8000

# Запускаємо FastAPI через uvicorn
# Тепер правильно — файл main.py лежить у корені, тому просто main:app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
