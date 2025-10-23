FROM python:3.11-slim

# Установка uv
RUN pip install uv

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml ./

# Устанавливаем зависимости с помощью uv
RUN uv pip install --system -r pyproject.toml

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]