FROM python:3.12-slim AS base

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY src ./src
COPY tests ./tests
COPY main.py ./main.py   

EXPOSE 8000

# ---------- СБОРКА + ТЕСТЫ ----------
FROM base AS test
WORKDIR /app
RUN pytest -q

# ---------- ФИНАЛЬНЫЙ ОБРАЗ ----------
FROM base AS final
WORKDIR /app
COPY --from=base /app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
